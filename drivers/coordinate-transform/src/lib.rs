#![no_std]

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Pose2D {
    pub x: f32,
    pub y: f32,
    pub yaw_rad: f32,
}

impl Pose2D {
    pub const fn new(x: f32, y: f32, yaw_rad: f32) -> Self {
        Self { x, y, yaw_rad }
    }
}

pub fn transform_pose(frame: Pose2D, local: Pose2D) -> Pose2D {
    let s = libm::sinf(frame.yaw_rad);
    let c = libm::cosf(frame.yaw_rad);
    let x = frame.x + c * local.x - s * local.y;
    let y = frame.y + s * local.x + c * local.y;
    Pose2D::new(x, y, normalize_angle(frame.yaw_rad + local.yaw_rad))
}

pub fn inverse_transform(frame: Pose2D, global: Pose2D) -> Pose2D {
    let dx = global.x - frame.x;
    let dy = global.y - frame.y;
    let s = libm::sinf(frame.yaw_rad);
    let c = libm::cosf(frame.yaw_rad);
    let x = c * dx + s * dy;
    let y = -s * dx + c * dy;
    Pose2D::new(x, y, normalize_angle(global.yaw_rad - frame.yaw_rad))
}

pub fn normalize_angle(mut angle: f32) -> f32 {
    const PI: f32 = core::f32::consts::PI;
    const TAU: f32 = 2.0 * PI;
    while angle > PI {
        angle -= TAU;
    }
    while angle <= -PI {
        angle += TAU;
    }
    angle
}

#[cfg(test)]
mod tests {
    use super::*;

    fn close(a: f32, b: f32) -> bool {
        (a - b).abs() < 1e-4
    }

    #[test]
    fn identity_transform_keeps_pose() {
        let frame = Pose2D::new(0.0, 0.0, 0.0);
        let local = Pose2D::new(1.2, -0.3, 0.4);
        let out = transform_pose(frame, local);
        assert!(close(out.x, local.x));
        assert!(close(out.y, local.y));
        assert!(close(out.yaw_rad, local.yaw_rad));
    }

    #[test]
    fn quarter_turn_rotation_is_correct() {
        let frame = Pose2D::new(0.0, 0.0, core::f32::consts::FRAC_PI_2);
        let local = Pose2D::new(1.0, 0.0, 0.0);
        let out = transform_pose(frame, local);
        assert!(close(out.x, 0.0));
        assert!(close(out.y, 1.0));
    }

    #[test]
    fn inverse_recovers_original_local_pose() {
        let frame = Pose2D::new(2.0, -1.0, 0.3);
        let local = Pose2D::new(-0.6, 1.4, -0.5);
        let global = transform_pose(frame, local);
        let recovered = inverse_transform(frame, global);
        assert!(close(recovered.x, local.x));
        assert!(close(recovered.y, local.y));
        assert!(close(recovered.yaw_rad, local.yaw_rad));
    }
}
