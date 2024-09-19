import unittest
import os
import numpy as np
from osgeo import gdal
from processor import process_geotiff

class TestProcessor(unittest.TestCase):
    def setUp(self):
        # Create a sample GeoTIFF for testing
        self.input_path = 'test_input.tif'
        self.output_path = 'test_output.tif'
        
        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(self.input_path, 10, 10, 1, gdal.GDT_Float32)
        
        # Fill with sample data
        data = np.random.rand(10, 10) * 100
        dataset.GetRasterBand(1).WriteArray(data)
        dataset = None

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_process_geotiff(self):
        # Process the test GeoTIFF
        process_geotiff(self.input_path, self.output_path)

        # Check if output file was created
        self.assertTrue(os.path.exists(self.output_path))

        # Verify the output data
        input_ds = gdal.Open(self.input_path)
        output_ds = gdal.Open(self.output_path)

        input_data = input_ds.GetRasterBand(1).ReadAsArray()
        output_data = output_ds.GetRasterBand(1).ReadAsArray()

        # Check if the output values are double the input values
        np.testing.assert_array_almost_equal(output_data, input_data * 2)

        # Check if projection and geotransform are preserved
        self.assertEqual(input_ds.GetProjection(), output_ds.GetProjection())
        self.assertEqual(input_ds.GetGeoTransform(), output_ds.GetGeoTransform())

        input_ds = None
        output_ds = None

if __name__ == '__main__':
    unittest.main()