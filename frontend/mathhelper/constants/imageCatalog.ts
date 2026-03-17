/**
 * Image catalog — maps image IDs (used by the AI) to local asset require() calls.
 * When the AI includes an image ID in its response, we look it up here to display it.
 */

const IMAGE_CATALOG: Record<string, any> = {
  // Chapter 1.1 — What Is an Angle?
  '1_1_angle_parts_labeled': require('../assets/images/ch1/1_1_angle_parts_labeled.png'),
  '1_1_positive_negative_rotation': require('../assets/images/ch1/1_1_positive_negative_rotation.png'),
  '1_1_angle_types': require('../assets/images/ch1/1_1_angle_types.png'),
  '1_1_complementary_supplementary': require('../assets/images/ch1/1_1_complementary_supplementary.png'),

  // Chapter 1.2 — Degree Measure
  '1_2_full_half_quarter_rotation': require('../assets/images/ch1/1_2_full_half_quarter_rotation.png'),
  '1_2_dms_breakdown': require('../assets/images/ch1/1_2_dms_breakdown.png'),
  '1_2_coterminal_angles': require('../assets/images/ch1/1_2_coterminal_angles.png'),

  // Chapter 1.3 — Radian Measure
  '1_3_radian_definition': require('../assets/images/ch1/1_3_radian_definition.png'),
  '1_3_full_circle_2pi': require('../assets/images/ch1/1_3_full_circle_2pi.png'),
  '1_3_common_radian_values': require('../assets/images/ch1/1_3_common_radian_values.png'),

  // Chapter 1.4 — Converting Degrees and Radians
  '1_4_conversion_diagram': require('../assets/images/ch1/1_4_conversion_diagram.png'),
  '1_4_common_conversions_table': require('../assets/images/ch1/1_4_common_conversions_table.png'),

  // Chapter 1.5 — Arc Length and Sector Area
  '1_5_arc_length_diagram': require('../assets/images/ch1/1_5_arc_length_diagram.png'),
  '1_5_sector_area_diagram': require('../assets/images/ch1/1_5_sector_area_diagram.png'),
  '1_5_clock_example': require('../assets/images/ch1/1_5_clock_example.png'),

  // Chapter 1.6 — Angular and Linear Speed
  '1_6_angular_speed_diagram': require('../assets/images/ch1/1_6_angular_speed_diagram.png'),
  '1_6_linear_vs_angular': require('../assets/images/ch1/1_6_linear_vs_angular.png'),
  '1_6_gear_relationship': require('../assets/images/ch1/1_6_gear_relationship.png'),
};

/** Look up an image by its AI-referenced ID. Returns the require() source or null. */
export function getImageSource(imageId: string): any | null {
  return IMAGE_CATALOG[imageId] ?? null;
}

/** Check if an image ID exists in the catalog. */
export function hasImage(imageId: string): boolean {
  return imageId in IMAGE_CATALOG;
}

export default IMAGE_CATALOG;
