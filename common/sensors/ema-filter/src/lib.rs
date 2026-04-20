#![cfg_attr(not(test), no_std)]

/// Exponential Moving Average filter for scalar sensor streams.
///
/// `alpha` controls responsiveness (0.0 < alpha <= 1.0):
/// - closer to 1.0: less smoothing, faster response
/// - closer to 0.0: more smoothing, slower response
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct EmaFilter {
    alpha: f32,
    state: Option<f32>,
}

impl EmaFilter {
    /// Create a new filter from alpha.
    pub fn new(alpha: f32) -> Result<Self, EmaError> {
        if !(0.0 < alpha && alpha <= 1.0) {
            return Err(EmaError::InvalidAlpha(alpha));
        }

        Ok(Self { alpha, state: None })
    }

    /// Returns configured alpha.
    pub fn alpha(&self) -> f32 {
        self.alpha
    }

    /// Returns true when the filter has consumed at least one sample.
    pub fn is_initialized(&self) -> bool {
        self.state.is_some()
    }

    /// Returns current state if initialized.
    pub fn state(&self) -> Option<f32> {
        self.state
    }

    /// Consume a new measurement and return filtered output.
    pub fn update(&mut self, sample: f32) -> f32 {
        let next = match self.state {
            Some(prev) => self.alpha * sample + (1.0 - self.alpha) * prev,
            None => sample,
        };

        self.state = Some(next);
        next
    }

    /// Reinitialize the filter state with a seed measurement.
    pub fn reset(&mut self, seed: f32) {
        self.state = Some(seed);
    }

    /// Clear any internal state so the next `update` seeds from input.
    pub fn clear(&mut self) {
        self.state = None;
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum EmaError {
    InvalidAlpha(f32),
}

#[cfg(test)]
mod tests {
    use super::*;

    fn almost_eq(a: f32, b: f32, eps: f32) {
        assert!((a - b).abs() <= eps, "{} != {} (eps={})", a, b, eps);
    }

    #[test]
    fn rejects_invalid_alpha_values() {
        assert!(matches!(EmaFilter::new(0.0), Err(EmaError::InvalidAlpha(_))));
        assert!(matches!(EmaFilter::new(-0.1), Err(EmaError::InvalidAlpha(_))));
        assert!(matches!(EmaFilter::new(1.01), Err(EmaError::InvalidAlpha(_))));
    }

    #[test]
    fn accepts_valid_alpha_bounds() {
        assert!(EmaFilter::new(0.0001).is_ok());
        assert!(EmaFilter::new(1.0).is_ok());
    }

    #[test]
    fn first_update_seeds_state() {
        let mut filter = EmaFilter::new(0.25).unwrap();
        let out = filter.update(12.5);

        almost_eq(out, 12.5, 1e-6);
        assert!(filter.is_initialized());
        almost_eq(filter.state().unwrap(), 12.5, 1e-6);
    }

    #[test]
    fn update_applies_ema_equation() {
        let mut filter = EmaFilter::new(0.2).unwrap();

        almost_eq(filter.update(10.0), 10.0, 1e-6);
        // next = 0.2*14 + 0.8*10 = 10.8
        almost_eq(filter.update(14.0), 10.8, 1e-6);
        // next = 0.2*4 + 0.8*10.8 = 9.44
        almost_eq(filter.update(4.0), 9.44, 1e-6);
    }

    #[test]
    fn alpha_one_tracks_input_without_smoothing() {
        let mut filter = EmaFilter::new(1.0).unwrap();

        almost_eq(filter.update(3.0), 3.0, 1e-6);
        almost_eq(filter.update(-7.0), -7.0, 1e-6);
        almost_eq(filter.update(42.0), 42.0, 1e-6);
    }

    #[test]
    fn reset_overwrites_internal_state() {
        let mut filter = EmaFilter::new(0.5).unwrap();
        filter.update(20.0);
        filter.reset(100.0);

        almost_eq(filter.state().unwrap(), 100.0, 1e-6);
        // next = 0.5*0 + 0.5*100 = 50
        almost_eq(filter.update(0.0), 50.0, 1e-6);
    }

    #[test]
    fn clear_drops_state_and_reseeds_on_next_update() {
        let mut filter = EmaFilter::new(0.3).unwrap();
        filter.update(20.0);
        filter.update(10.0);
        filter.clear();

        assert_eq!(filter.state(), None);
        almost_eq(filter.update(5.0), 5.0, 1e-6);
    }
}
