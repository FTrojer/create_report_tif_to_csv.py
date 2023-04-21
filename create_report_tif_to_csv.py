"""

@author: fabian trojer & tashi freyer | Geoville

Description: Open and read two .tif files and generate .csv file containing comparison statistics such as
-number of pixels per land cover class
-number of thematically (un)changed pixels
-fraction per land cover class
-fraction change per land cover class
-accuracy (assuming that first .tif file serves as ground truth)



             Necessary Parameters:
                 - path to .tif file 1 (e.g. r"C:\gv\test_area_raster.tif")
                 - path to .tif file 2 (e.g. r"C:\gv\test_area_raster.tif")
                 - output folder where generated .csv file is meant to be stored (r"C:\gv\BB")

"""
import csv
import pandas as pd
import rasterio
import numpy as np
from pathlib import Path


def create_report_tif_to_csv(tif_file_2018, tif_file_2021, output_folder):

    # OPEN TIF FILES -----------------------------------------------------
    dataset2018 = rasterio.open(tif_file_2018)
    dataset2021 = rasterio.open(tif_file_2021)
    outfolder = Path(output_folder)
    outpath = outfolder / "CLCBB_statistics.csv"

    # GET VALUES OF BAND
    array2018 = dataset2018.read(1)
    print("The shape of the 2018 file is:", array2018.shape)
    array2021 = dataset2021.read(1)
    print("The shape of the 2021 file is:", array2021.shape)

    # GET NUMBER OF CLASSES
    num_class = list(range(1, 12))
    print(num_class)

    # DEFINE YEARS
    years = {
        0: "2018",
        1: "2021"
    }

    # DEFINE LAND COVER CLASSES AND THEIR NAMES
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

    # PROJECT CRS FORMATTED: "EPSG:####"
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
        print("The pixel count of the class " + str(c) + " for 2018 file is:", ccount2018)
        print("The pixel count of the class " + str(c) + " for 2021 file is:", ccount2021)

        # SAVE COUNTS PER CLASS
        count2018.append(ccount2018)
        count2021.append((ccount2021))

    # CHANGE BETWEEN 2018 AND 2021
    difference_18_21 = [abs(ele) for ele in ([x - y for x, y in zip(count2018, count2021)])]

    # NO CHANGE BETWEEN 2018 AND 2021
    pixels_no_change = [x - y for x, y in zip(count2018, difference_18_21)]

    # ACCURACY PER CLASS
    accuracy = []
    for i in range(len(pixels_no_change)):
        if count2018[i] != 0:
            accuracy.append(pixels_no_change[i] / count2018[i])
        else:
            accuracy.append(0.0)

    # OVERALL ACCURACY
    class_weights = [pixels_no_change]
    class_accuracy = [accuracy]

    overall_accuracy = sum([w * a for w, a in zip(pixels_no_change, accuracy)]) / sum(pixels_no_change)

    print("Overall Accuracy: {:.2f}".format(overall_accuracy))

    # OPEN A NEW CSV FILE FOR WRITING--------------------------------------
    with open(outpath, 'w', newline='') as f:

        # CREATE A CSV WRITER OBJECT
        writer = csv.writer(f)

        # ADD CLCBB STATISTICS
        writer.writerow([f"CLCBB Validation Report"])
        writer.writerow([f"CLCBB"])

        # CREATE AN EMPTY ROW
        empty_row = []

        # WRITE THE EMPTY ROW TO THE CSV FILE
        writer.writerows([empty_row])

        df = pd.DataFrame({"2018": count2018,
                           "2021": count2021,
                           "difference_18_21": difference_18_21,
                           "pixels_no_change": pixels_no_change,
                           "accuracy/class": accuracy}).T

        df = df.rename(columns=land_cover_classes)
        print(df)
        df.to_csv(f, sep=",")

        # ADD OVERALL ACCURACY
        writer.writerow(['Overall accuracy:', '{:.2f}'.format(overall_accuracy)])

        # CALCULATE THE TOTAL NUMBER OF PIXELS FOR ALL LAND COVER CLASSES
        total_pixels_2018 = sum(count2018) + sum(difference_18_21)
        total_pixels_2021 = sum(count2021) + sum(difference_18_21)

        # GENERATE STATISTICS FOR EACH LAND COVER CLASS
        for index, land_cover in land_cover_classes.items():
            # CREATE AN EMPTY ROW
            separation_row = [f"-----------------------"]

            # WRITE THE EMPTY ROW TO THE CSV FILE
            writer.writerows([separation_row])

            writer.writerow([f"{index + 1} {land_cover} statistics\n\n"])

            # CALCULATE FRACTION OF PIXELS FOR EACH LAND COVER CLASS
            if total_pixels_2018 != 0:
                fraction_2018 = (count2018[index] + difference_18_21[index]) / total_pixels_2018 * 100
            else:
                fraction_2018 = 0

            if total_pixels_2021 != 0:
                fraction_2021 = (count2021[index] + difference_18_21[index]) / total_pixels_2021 * 100
            else:
                fraction_2021 = 0

            fraction_change = fraction_2021 - fraction_2018

            df = pd.DataFrame({
                "2018": count2018[index],
                "2021": count2021[index],
                "difference_18_21": difference_18_21[index],
                "pixels_no_change": pixels_no_change[index],
                "class_accuracy": accuracy[index],
                "fraction_2018(%)": fraction_2018,
                "fraction_2021(%)": fraction_2021,
                "fraction_change(%)": fraction_change,
            }, index=['Total pixels']).T

            df.to_csv(f, sep=",")


create_report_tif_to_csv(r"C:\gv\test_area_raster.tif", r"C:\gv\BB\test_area_raster2.tif", r"C:\gv\BB")
