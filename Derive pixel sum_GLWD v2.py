import os
from qgis.core import (
    QgsRasterLayer,
    QgsRasterDataProvider
)
import csv

# Folder where clipped TIFFs are stored
folder_path = r'C:/Users/petra/Documents/Summer project/GLWD/GLWD_output/Sweden tifs'

# Output CSV file
output_csv = os.path.join(folder_path, 'sweden_raster_stats.csv')

# Prepare output
output_data = []
output_data.append(['Class', 'Filename', 'Sum', 'Hectares'])

# Loop through all .tif files
for filename in os.listdir(folder_path):
    if filename.endswith('.tif') and filename.startswith('SWE'):
        raster_path = os.path.join(folder_path, filename)
        rlayer = QgsRasterLayer(raster_path, filename)
        if not rlayer.isValid():
            print(f"Invalid raster: {filename}")
            continue
        stats = rlayer.dataProvider().bandStatistics(1)
        pixel_sum = stats.sum
        hectares = pixel_sum / 10
        # Extract class from filename (e.g., SWE17.tif → 17)
        class_number = filename.replace('SWE', '').replace('.tif', '')
        output_data.append([class_number, filename, pixel_sum, hectares])
		
# Write to CSV
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output_data)
print(f"\n✅ Stats saved to:\n{output_csv}")
