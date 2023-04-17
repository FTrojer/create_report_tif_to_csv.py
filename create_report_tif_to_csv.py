import csv
import pandas as pd
import rasterio
import numpy as np

def create_report_tif_to_csv():

        # OPEN TIF FILES -----------------------------------------------------
        dataset2018 = rasterio.open(r"C:\Users\tashi\temp\Reportcreator\test_area_raster.tif")
        dataset2021 = rasterio.open(r"C:\Users\tashi\temp\Reportcreator\test_area_raster_2.tif")

        # GET VALUES OF BAND
        array2018 = dataset2018.read(1)
        print("The shape of the 2018 file is:", array2018.shape)
        array2021 = dataset2021.read(1)
        print("The shape of the 2021 file is:", array2021.shape)

        # NUMBER OF CLASSES
        num_class = list(range(1, 12))
        print(num_class)

        # DEFINE YEARS
        years = {
            0: "2018",
            1: "2021"
        }

        # DEFINE THE LAND COVER CLASSES AND THEIR NAMES
        land_cover_classes = {
            0: "Sealed",
            1: "Woody – needle leaved trees",
            2: "Woody – broadleaved, deciduous trees",
            3: "Woody – broadleaved, evergreen trees",
            4: "Woody – shrubs",
            5: "Permanent herbaceous",
            6: "Periodically herbaceous",
            7: "Lichens and mosses",
            8: "Sparsely/non vegetated",
            9: "Water",
            10: "Snow and ice"
        }

        # PROJECT CRS FORMATED: "EPSG:####"
        project_crs = "epsg:3035"

        # COUNT OF PIXELS PER CLASS
        count2018 = []
        count2021 = []

        # LOOP OVER CLASSES
        for c in num_class:
            cind2018 = np.where(array2018 == c)
            cind2021 = np.where(array2021 == c)

            # PIXEL COUNT OF CLASS
            ccount2018 = cind2018[0].size
            ccount2021 = cind2021[0].size
            difference_2018_2021 = abs(ccount2018-ccount2021)
            pixel_no_change = ccount2018 - difference_2018_2021
            if 
            accurancy = ccount2018/pixel_no_change

            print("The pixel count of the class " + str(c) + " for 2018 file is:", ccount2018)
            print("The pixel count of the class " + str(c) + " for 2021 file is:", ccount2021)

            # SAVE COUNTS PER CLASS
            count2018.append(ccount2018)
            count2021.append((ccount2021))

        difference_2018_2021 = [abs(ele) for ele in ([x - y for x, y in zip(count2018, count2021)])]
        pixel_no_change =

        # OPEN A NEW CSV FILE FOR WRITING--------------------------------------
        with open(r'C:\Users\tashi\temp\Reportcreator\CLCBB_statistics.csv', 'w', newline='') as f:
            # CREATE A CSV WRITER OBJECT-----------------------------------------
            writer = csv.writer(f)

            # ADD CLCBB STATISTICS
            writer.writerow([f"CLCBB Validation Report\n\n"])
            writer.writerow([f"CLCBB\n\n"])

            #
            df = pd.DataFrame({"2018": count2018,
                               "2021": count2021,
                               "difference_18_21_per_class": difference_2018_2021,

                               }).T

            #sum up number of all changed pixels
            df = df.rename(columns=land_cover_classes)
            print(df)
            pixels_changed_total = sum(df["difference_18_21_per_class"])
            print(pixels_changed_total)
            df.to_csv(f, sep=",")

            # ADD OVERALL ACCURACY







create_report_tif_to_csv()
