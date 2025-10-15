import ansa
from ansa import base, mesh, utils, constants, batchmesh
import os, sys


def merge_ansa_file(ansa_file_path, original_model_name):
    """
    Merge an ANSA file into the current session using the utils.Merge function.
    """
    try:
        print(f"\nMerging ANSA file: {ansa_file_paCVth}")

        # Ensure the current deck is Abaqus
        if base.CurrentDeck() != constants.ABAQUS:
            base.SetCurrentDeck(constants.ABAQUS)
            print("Current deck set to ABAQUS.")

        # Merge the ANSA file
        utils.Merge(
            filename=ansa_file_path,
            directory="",
            property_offset="keep-new",
            material_offset="keep-old",
            set_offset="offset",
            merge_sets_by_name=True,
            paste_nodes_by_name=True,
            paste_nodes_by_name_tolerance=0.02,
            paste_cons_by_name=False,
            merge_parts=True,
            autoposition_parts=False,
        )
        print("ANSA file merged successfully.")
    except Exception as e:
        print(f"Error merging ANSA file: {e}")


def get_parts_from_module_id_range(start_id, end_id):
    """
    Retrieve parts from a given range of Module IDs.
    """
    parts_list = []
    for module_id in range(start_id, end_id + 1):
        part = base.GetPartFromModuleId(str(module_id))
        if part:
            parts_list.append(part)

    if not parts_list:
        print("Nothing found in the module ID range provided.")

    return parts_list


def batch_mesh_and_improve(original_model_name, output_folder):
    """
    Perform batch meshing and improvement for multiple parts in the model.
    Save the file with the name <original_filename>_firstmesh.ansa in the specified output folder.
    Returns the new file path.
    """
    print("\nCollecting batch mesh sessions...")
    sessions_array = base.CollectEntities(constants.ABAQUS, None, "BATCH_MESH_SESSION", False)
    if not sessions_array:
        print("No batch mesh sessions found in the imported file.")
        return None
    selected_session = sessions_array[0]
    print(f"Selected session: {selected_session._name}")

    # Get parts from a module ID range
    start_module_id, end_module_id = 1, 100  # Increased search range
    parts = get_parts_from_module_id_range(start_module_id, end_module_id)
    if not parts:
        return None

    # Add the parts to the session contents
    try:
        batchmesh.AddPartToSession(parts, selected_session)
        print("Parts added to the session successfully.")
    except Exception as e:
        print(f"Error adding parts to the session: {e}")
        return None

    # Copy session parameters and run batch meshing
    try:
        batchmesh.CopySessionParameters(selected_session, mesh_parameters=True, quality_criteria=True)
        print("Mesh parameters and quality criteria copied successfully.")
    except Exception as e:
        print(f"Error copying session parameters: {e}")
        return None

    try:
        print("\nRunning batch meshing...")
        status = batchmesh.RunSession(selected_session)
        if not status:
            print("Batch meshing failed.")
            return None
        print("Batch meshing completed successfully.")
    except Exception as e:
        print(f"Error during batch meshing: {e}")
        return None

    # **Ensure the output folder exists**
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # **Construct the correct output file path**
    original_file_base_name = os.path.basename(original_model_name)
    new_file_path = os.path.join(output_folder, f"{os.path.splitext(original_file_base_name)[0]}_firstmesh.ansa")

    # **Save the current model as the new file**
    try:
        base.SaveAs(new_file_path)
        print(f"\u2705 File successfully saved at: {new_file_path}")
        return new_file_path  # Return the new file path
    except Exception as e:
        print(f"\u274c Error saving file: {e}")
        return None


def main():
    """
    Main function to execute the workflow.
    """
    ansa_file_path = r"/Shashank/Python/STL_mesh_file.ansa"
    output_folder = r"Shashank/Python/ansa_test/output_mesh_from_script"

    # **Step 1: Capture the original filename BEFORE merging**
    original_model_names = base.GetAnsaModelSourceFileNames(base.GetCurrentAnsaModel())

    if not original_model_names:
        print("\u274c Error: Could not retrieve the original model name.")
        return

    # Take the first file name if multiple are returned
    original_model_name = original_model_names[0]

    print("\nStep 1: Merging ANSA file...")
    merge_ansa_file(ansa_file_path, original_model_name)

    print("\nStep 2: Performing batch meshing and improvement...")
    new_file_path = batch_mesh_and_improve(original_model_name, output_folder)

    if new_file_path:
        print(f"\nThe modified file has been saved at: {new_file_path}")
    else:
        print("Batch meshing failed, no file saved.")

    base.CloseAnsaWindow(0)
    sys.exit()
if __name__ == "__main__":
    main()
 
