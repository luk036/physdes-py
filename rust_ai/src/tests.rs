//! Test module for physdes-rs

#[cfg(test)]
mod tests {
    use crate::interval::Interval;
    use crate::point::Point;
    use crate::vector2::Vector2;
    use crate::recti::{Rectangle, VSegment, HSegment};
    use crate::generic::{overlap, contain, min_dist, Overlaps, Contains, MinDistWith};

    #[test]
    fn test_interval_basic() {
        let interval1 = Interval::new(1, 5);
        let interval2 = Interval::new(3, 7);
        let interval3 = Interval::new(6, 8);
        
        assert!(interval1.overlaps(&interval2));
        assert!(!interval1.overlaps(&interval3));
        assert_eq!(interval1.width(), 4);
        assert_eq!(interval2.width(), 4);
    }
    
    #[test]
    fn test_point_basic() {
        let point1 = Point::new(3, 4);
        let point2 = Point::new(3, 4);
        let point3 = Point::new(5, 6);
        
        assert!(point1.overlaps(&point2));
        assert!(!point1.overlaps(&point3));
        assert_eq!(point1.x(), &3);
        assert_eq!(point1.y(), &4);
    }
    
    #[test]
    fn test_vector2_basic() {
        let v1 = Vector2::new(1, 2);
        let v2 = Vector2::new(3, 4);
        let v3 = v1 + v2;
        
        assert_eq!(v3.x(), &4);
        assert_eq!(v3.y(), &6);
        
        let v4 = v2 - v1;
        assert_eq!(v4.x(), &2);
        assert_eq!(v4.y(), &2);
        
        let v5 = v1 * 2;
        assert_eq!(v5.x(), &2);
        assert_eq!(v5.y(), &4);
    }
    
    #[test]
    fn test_rectangle_basic() {
        let rect1 = Rectangle::new(
            Interval::new(1, 5),
            Interval::new(2, 6)
        );
        
        let rect2 = Rectangle::new(
            Interval::new(3, 7),
            Interval::new(4, 8)
        );
        
        let rect3 = Rectangle::new(
            Interval::new(10, 15),
            Interval::new(10, 15)
        );
        
        assert!(rect1.overlaps(&rect2));
        assert!(!rect1.overlaps(&rect3));
        
        let ll = rect1.ll();
        assert_eq!(ll.x(), &1);
        assert_eq!(ll.y(), &2);
        
        let ur = rect1.ur();
        assert_eq!(ur.x(), &5);
        assert_eq!(ur.y(), &6);
    }
    
    #[test]
    fn test_generic_functions() {
        let interval1 = Interval::new(1, 5);
        let interval2 = Interval::new(3, 7);
        
        assert!(overlap(&interval1, &interval2));
        assert!(!contain(&interval1, &interval2));
        
        let dist = min_dist(&interval1, &interval2);
        assert_eq!(dist, 0);  // They overlap
        
        let interval3 = Interval::new(10, 15);
        let dist2 = min_dist(&interval1, &interval3);
        assert_eq!(dist2, 5);  // 10 - 5 = 5
    }
    
    #[test]
    fn test_segments() {
        let vseg = VSegment::new(5, Interval::new(1, 10));
        let hseg = HSegment::new(Interval::new(1, 10), 5);
        
        let point_on_vseg = Point::new(5, 3);
        let point_on_hseg = Point::new(3, 5);
        
        assert!(vseg.contains(&point_on_vseg));
        assert!(hseg.contains(&point_on_hseg));
        
        let flipped_vseg = vseg.flip();
        assert_eq!(flipped_vseg.x_interval(), vseg.y_interval());
        assert_eq!(flipped_vseg.y(), vseg.x());
    }
}