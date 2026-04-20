use anyhow::{bail, Context, Result};
use clap::Parser;
use rppal::gpio::{Gpio, OutputPin};
use std::{thread, time::Duration};

/// Simple servo controller for Raspberry Pi using rppal GPIO + software PWM.
///
/// Typical servo expectations:
/// - 50 Hz (20 ms period)
/// - pulse width ~ 1.0 ms (min) to ~ 2.0 ms (max)
/// - 1.5 ms is typically center
#[derive(Parser, Debug)]
#[command(author, version, about)]
struct Args {
    /// BCM GPIO pin number (not physical pin number). Example: 18
    #[arg(long, default_value_t = 18)]
    gpio: u8,

    /// Target angle in degrees (0..=180). Ignored when --normalized is set.
    #[arg(long, default_value_t = 90)]
    angle: u16,

    /// Optional normalized command in range [-1.0, 1.0] (e.g. joystick input).
    #[arg(long)]
    normalized: Option<f32>,

    /// Deadband applied around 0.0 for normalized input (0.0..1.0).
    #[arg(long, default_value_t = 0.05)]
    deadband: f32,

    /// How many seconds to hold the signal (most servos keep position while powered)
    #[arg(long, default_value_t = 3)]
    hold_s: u64,

    /// Servo pulse min in microseconds (typical 1000)
    #[arg(long, default_value_t = 1000)]
    min_us: u32,

    /// Servo pulse max in microseconds (typical 2000)
    #[arg(long, default_value_t = 2000)]
    max_us: u32,

    /// PWM frequency in Hz (typical 50)
    #[arg(long, default_value_t = 50)]
    hz: u32,
}

fn angle_to_pulse_us(angle: u16, min_us: u32, max_us: u32) -> u32 {
    let a = angle.min(180) as u32;
    min_us + (a * (max_us - min_us) / 180)
}

fn normalized_to_pulse_us(command: f32, deadband: f32, min_us: u32, max_us: u32) -> Result<u32> {
    if !command.is_finite() {
        bail!("normalized command must be finite");
    }
    if !(0.0..1.0).contains(&deadband) {
        bail!("deadband must be in [0.0, 1.0)");
    }

    let center = (min_us + max_us) as f32 / 2.0;
    let half_range = (max_us - min_us) as f32 / 2.0;
    let cmd = command.clamp(-1.0, 1.0);

    if cmd.abs() <= deadband {
        return Ok(center.round() as u32);
    }

    let sign = cmd.signum();
    let magnitude = ((cmd.abs() - deadband) / (1.0 - deadband)).clamp(0.0, 1.0);
    let scaled = sign * magnitude;
    let pulse = center + (scaled * half_range);

    Ok(pulse.round().clamp(min_us as f32, max_us as f32) as u32)
}

fn run_soft_pwm(pin: &mut OutputPin, pulse_us: u32, hz: u32, hold_s: u64) -> Result<()> {
    if hz == 0 {
        bail!("hz must be > 0");
    }
    let period_us: u32 = 1_000_000 / hz;
    if pulse_us >= period_us {
        bail!("pulse_us ({pulse_us}) must be less than period_us ({period_us})");
    }

    let high = Duration::from_micros(pulse_us as u64);
    let low = Duration::from_micros((period_us - pulse_us) as u64);

    let cycles = hz as u64 * hold_s;
    for _ in 0..cycles {
        pin.set_high();
        thread::sleep(high);
        pin.set_low();
        thread::sleep(low);
    }
    Ok(())
}

fn main() -> Result<()> {
    let args = Args::parse();

    if args.angle > 180 {
        bail!("angle must be 0..=180");
    }
    if args.min_us >= args.max_us {
        bail!("min_us must be < max_us");
    }
    if !(0.0..1.0).contains(&args.deadband) {
        bail!("deadband must be in [0.0, 1.0)");
    }

    let pulse_us = match args.normalized {
        Some(command) => normalized_to_pulse_us(command, args.deadband, args.min_us, args.max_us)?,
        None => angle_to_pulse_us(args.angle, args.min_us, args.max_us),
    };

    let gpio = Gpio::new().context("Failed to access GPIO (try running with sudo)")?;
    let mut pin = gpio
        .get(args.gpio)
        .with_context(|| format!("BCM GPIO {} not available", args.gpio))?
        .into_output_low();

    let source = match args.normalized {
        Some(command) => format!("normalized={command:.3} deadband={:.3}", args.deadband),
        None => format!("angle={}", args.angle),
    };

    println!(
        "GPIO={} {} => pulse={}us @ {}Hz for {}s",
        args.gpio, source, pulse_us, args.hz, args.hold_s
    );

    run_soft_pwm(&mut pin, pulse_us, args.hz, args.hold_s)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::normalized_to_pulse_us;

    #[test]
    fn normalized_center_in_deadband_maps_to_center() {
        assert_eq!(normalized_to_pulse_us(0.0, 0.1, 1000, 2000).unwrap(), 1500);
        assert_eq!(normalized_to_pulse_us(0.08, 0.1, 1000, 2000).unwrap(), 1500);
        assert_eq!(normalized_to_pulse_us(-0.1, 0.1, 1000, 2000).unwrap(), 1500);
    }

    #[test]
    fn normalized_extremes_map_to_bounds() {
        assert_eq!(normalized_to_pulse_us(1.0, 0.1, 1000, 2000).unwrap(), 2000);
        assert_eq!(normalized_to_pulse_us(-1.0, 0.1, 1000, 2000).unwrap(), 1000);
    }

    #[test]
    fn normalized_midpoint_after_deadband_maps_linearly() {
        assert_eq!(normalized_to_pulse_us(0.55, 0.1, 1000, 2000).unwrap(), 1750);
        assert_eq!(
            normalized_to_pulse_us(-0.55, 0.1, 1000, 2000).unwrap(),
            1250
        );
    }

    #[test]
    fn normalized_input_is_clamped() {
        assert_eq!(normalized_to_pulse_us(2.0, 0.1, 1000, 2000).unwrap(), 2000);
        assert_eq!(normalized_to_pulse_us(-3.0, 0.1, 1000, 2000).unwrap(), 1000);
    }

    #[test]
    fn invalid_deadband_returns_error() {
        assert!(normalized_to_pulse_us(0.0, 1.0, 1000, 2000).is_err());
    }
}
