import pickle
import csv
import pandas as pd
import os

# Open the pickle file and load the dictionary
def create_report_csv():
    with open(r"C:\Users\tashi\temp\Reportcreator\input_dict_30SVH.pickle", 'rb') as f:
        input_dict = pickle.load(f)

    # Open a new CSV file for writing
    with open(r'C:\Users\tashi\temp\Reportcreator\input_dict_30SVH.csv', 'w', newline='') as f:
        # Create a CSV writer object
        writer = csv.writer(f)

        # Add BVL statistics
        writer.writerow([f"HER/GRA (BVL) Validation Report for {input_dict['tile_id']}\n\n"])
        writer.writerow([f"BVL Statistics\n\n"])

        df = pd.DataFrame(input_dict['validation']['statistics']).T
        df = df.rename(columns={1: "Herbaceous", 2: "Coniferous", 3: "Broadleaved",
                                4: "Crop land", 5: "Tree crops",
                                6: "Herb/Tree cover", 7: "Herb/Crops", 8: "other"})
        df.to_csv(f, sep=",")

        # Add threshold and accuracy for BVL
        writer.writerow([f"Best threshold: {input_dict['validation']['best_threshold']:.3f}"])
        writer.writerow([f"Best accuracy: {input_dict['validation']['accuracy']:.3f}"])


        # Add HER statistics
        writer.writerow([f"## HER Statistics\n"])

        df = pd.DataFrame([value["HER_binary"] for key, value in input_dict["processing"]["statistics"].items()])
        df["year"] = [key for key, value in input_dict["processing"]["statistics"].items()]
        df = df.set_index("year").sort_index()
        df = df.rename(columns={"abs": "Pixel count", "frac": "HER fraction", "abs_change": "Pixel count change",
                                "frac_change": "HER fraction change"})
        df.to_csv(f, sep=",")

        # Add threshold and accuracy for HER
        writer.writerow([f"Best threshold: {input_dict['processing']['best_threshold']:.3f}"])
        writer.writerow([f"Best accuracy: {input_dict['processing']['accuracy']:.3f}"])

        # Add GRA statistics
        writer.writerow([f"## GRA Statistics\n"])

        df = pd.DataFrame([value["GRA_binary"] for key, value in input_dict["processing"]["statistics"].items()])
        df["year"] = [key for key, value in input_dict["processing"]["statistics"].items()]
        df = df.set_index("year").sort_index()
        df = df.rename(columns={"abs": "Pixel count", "frac": "GRA fraction", "abs_change": "Pixel count change",
                                "frac_change": "GRA fraction change"})
        df.to_csv(f, sep=",")

        # Add BVL validation report - OK
        writer.writerow([f"## BVL Validation report"])

        if input_dict["validation"]["passed"]:
            writer.writerow(["  -  OK\n"])
        else:
            writer.writerow(["  -  NOT OK\n"])
        report_df = pd.DataFrame(input_dict["validation"]["report"])
        report_df.to_csv(f, sep=",")

        # Add HER/GRA Validation report - NOT OK
        writer.writerow([f"## HER/GRA Validation report"])

        if input_dict["processing"]["passed"]:
            writer.writerow(["  -  OK\n"])
        else:
            writer.writerow(["  -  NOT OK\n"])
        report_df = pd.DataFrame(input_dict["processing"]["report"])
        report_df.to_csv(f, sep=",")



        print(report_df)

create_report_csv()