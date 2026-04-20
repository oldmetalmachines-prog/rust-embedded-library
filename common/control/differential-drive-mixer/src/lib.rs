/// Differential drive mixer for skid-steer or tank-drive robots.
///
/// Accepts normalized throttle/steering inputs and outputs normalized left/right
/// motor commands with configurable deadband and output limits.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct DifferentialDriveMixer {
    deadband: f32,
    max_output: f32,
}

impl DifferentialDriveMixer {
    /// Create a new mixer.
    ///
    /// - `deadband` must be in `[0.0, 1.0)`
    /// - `max_output` must be in `(0.0, 1.0]`
    pub fn new(deadband: f32, max_output: f32) -> Result<Self, String> {
        if !(0.0..1.0).contains(&deadband) {
            return Err("deadband must be in [0.0, 1.0)".to_string());
        }
        if !(0.0..=1.0).contains(&max_output) || max_output == 0.0 {
            return Err("max_output must be in (0.0, 1.0]".to_string());
        }

        Ok(Self {
            deadband,
            max_output,
        })
    }

    /// Mix throttle and steering into left/right motor outputs.
    ///
    /// Input and output ranges are normalized to `[-1.0, 1.0]` before applying
    /// `max_output` clamping/scaling.
    pub fn mix(&self, throttle: f32, steering: f32) -> (f32, f32) {
        let t = apply_deadband(throttle.clamp(-1.0, 1.0), self.deadband);
        let s = apply_deadband(steering.clamp(-1.0, 1.0), self.deadband);

        let mut left = t + s;
        let mut right = t - s;

        let peak = left.abs().max(right.abs());
        if peak > self.max_output {
            let scale = self.max_output / peak;
            left *= scale;
            right *= scale;
        }

        (
            left.clamp(-self.max_output, self.max_output),
            right.clamp(-self.max_output, self.max_output),
        )
    }
}

fn apply_deadband(value: f32, deadband: f32) -> f32 {
    let abs = value.abs();
    if abs < deadband {
        0.0
    } else {
        let scaled = (abs - deadband) / (1.0 - deadband);
        value.signum() * scaled
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn approx_eq(a: f32, b: f32) {
        assert!((a - b).abs() < 1e-6, "{a} != {b}");
    }

    #[test]
    fn constructor_accepts_valid_bounds() {
        assert!(DifferentialDriveMixer::new(0.0, 1.0).is_ok());
        assert!(DifferentialDriveMixer::new(0.2, 0.8).is_ok());
    }

    #[test]
    fn constructor_rejects_invalid_bounds() {
        assert!(DifferentialDriveMixer::new(-0.1, 1.0).is_err());
        assert!(DifferentialDriveMixer::new(1.0, 1.0).is_err());
        assert!(DifferentialDriveMixer::new(0.1, 0.0).is_err());
        assert!(DifferentialDriveMixer::new(0.1, 1.1).is_err());
    }

    #[test]
    fn deadband_zeroes_small_inputs() {
        let m = DifferentialDriveMixer::new(0.2, 1.0).unwrap();
        let (l, r) = m.mix(0.1, -0.19);
        approx_eq(l, 0.0);
        approx_eq(r, 0.0);
    }

    #[test]
    fn deadband_rescales_outside_threshold() {
        let m = DifferentialDriveMixer::new(0.2, 1.0).unwrap();
        let (l, r) = m.mix(0.6, 0.0);
        // ((0.6 - 0.2) / 0.8) = 0.5 on both tracks
        approx_eq(l, 0.5);
        approx_eq(r, 0.5);
    }

    #[test]
    fn steering_only_turns_in_place() {
        let m = DifferentialDriveMixer::new(0.0, 1.0).unwrap();
        let (l, r) = m.mix(0.0, 0.75);
        approx_eq(l, 0.75);
        approx_eq(r, -0.75);
    }

    #[test]
    fn clamps_inputs_before_mix() {
        let m = DifferentialDriveMixer::new(0.0, 1.0).unwrap();
        let (l, r) = m.mix(2.0, -2.0);
        approx_eq(l, 0.0);
        approx_eq(r, 1.0);
    }

    #[test]
    fn normalizes_when_combined_outputs_exceed_max() {
        let m = DifferentialDriveMixer::new(0.0, 1.0).unwrap();
        let (l, r) = m.mix(1.0, 0.5); // raw (1.5, 0.5), peak=1.5 -> scale 2/3
        approx_eq(l, 1.0);
        approx_eq(r, 1.0 / 3.0);
    }

    #[test]
    fn honors_custom_max_output() {
        let m = DifferentialDriveMixer::new(0.0, 0.5).unwrap();
        let (l, r) = m.mix(1.0, 1.0); // raw (2,0) -> scaled to (0.5,0.0)
        approx_eq(l, 0.5);
        approx_eq(r, 0.0);
    }

    #[test]
    fn symmetric_reverse_behavior() {
        let m = DifferentialDriveMixer::new(0.1, 1.0).unwrap();
        let (lf, rf) = m.mix(0.7, -0.3);
        let (lr, rr) = m.mix(-0.7, 0.3);
        approx_eq(lf, -lr);
        approx_eq(rf, -rr);
    }
}
