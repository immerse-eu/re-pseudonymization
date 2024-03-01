import pandas as pd
import os
import openpyxl


if __name__ == '__main__':
    # specify filename for id file
    id_filename = "Immerse-IDs_for_repseudo.csv"
    # sensing data output subfolder name
    sensing_data_output = "./output/sensing_data"
    # specify pre-string for new pseudonyms
    project_re_pseudo_id = "01_03_2024-Koppe-"
    # specify all sensing filenames
    sensing_file_names = ["Master_Activity.xlsx", "Master_AppUsage.xlsx", "Master_DeviceRunning.xlsx", "Master_DisplayOn.xlsx", "Master_Location.xlsx", "Master_NotificationLog.xlsx", "Master_Steps.xlsx"]
    # specify all TherapyDesigner filenames
    therapy_designer_file_names = ["Bierbeek_final.xlsx", "Bratislava_final.xlsx", "Kosice_final.xlsx", "Leuven_final.xlsx", "Lothian_CAMSH_final.xlsx", "Lothian_final.xlsx", "Mannheim_final.xlsx"]

    # create not existing output subfolder for sensing data

    if not os.path.exists(sensing_data_output):
        os.makedirs(sensing_data_output)
    # create not existing output subfolder for TherapyDesigner data
    therapy_desinger_data_output = "./output/TherapyDesigner_data"
    if not os.path.exists(therapy_desinger_data_output):
        os.makedirs(therapy_desinger_data_output)

    # read in id data
    id_data = pd.read_csv("./input/" + id_filename)

    # iterate through subfolders and included files
    for subdir, dirs, files in os.walk("./input"):
        for file in files:
            # do not use the id files but only the data files
            if not (file == "Immerse-IDs_for_repseudo.csv" or file == "Immerse-IDs_for_repseudo.xlsx"):
                print(file + " started.")
                # read data file in
                file_data = pd.read_excel(os.path.join(subdir, file))
                # iterate through all rows of the id file and replace corresponding ids with new pseudonyms
                for index, row in id_data.iterrows():
                    file_data.replace(row.iloc[0], row.iloc[1], inplace=True)

                    # print every 50 rows a message
                    if index % 50 == 0:
                        print(str(index+1) + " / " + str(len(id_data)) + " IDs replaced.")
                # drop columns with identification data in sensing data
                if file in sensing_file_names:
                    file_data = file_data.drop(["StudyName", "probandID(moviID)"], axis=1)
                    subfolder_for_export = "sensing_data/"

                # drop columns with identification data in TheradyDesigner data
                else:
                    file_data = file_data.drop("study_name", axis=1)
                    subfolder_for_export = "TherapyDesigner_data/"

                # save file to output folder
                file_data.to_excel("./output/" + subfolder_for_export + file, index=False)
                print(file + " finished.")
