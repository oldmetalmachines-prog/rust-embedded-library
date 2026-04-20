# differential-drive-mixer

Small Rust utility for differential/skid-steer motor mixing.

## Features

- Clamps throttle and steering inputs to `[-1.0, 1.0]`
- Applies configurable deadband with range-preserving rescale
- Mixes to left/right outputs via:
  - `left = throttle + steering`
  - `right = throttle - steering`
- Normalizes outputs to a configurable max magnitude

## Test

```bash
cargo test -p differential-drive-mixer
```
