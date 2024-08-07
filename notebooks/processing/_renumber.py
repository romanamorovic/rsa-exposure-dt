import math
import os
import pickle
import subprocess

import _file_paths as fp


RESULT_CODE_TO_STATUS_MAPPING = {
    0: 'ok',
    4: 'non-antibody-chain',
    5: 'single-chain',
    6: 'alignment-failed',
    7: 'hl-not-paired',
    8: 'chain-not-numbered'
}


def renumber(input_dir_path: str, 
             filename: str, 
             output_dir_path: str,
             final_numbering_scheme: str) -> dict:
    """
    Call cleanup_mAb_renumberer script
    Handle the results
    
    @returns dict - structure_name => string, status => string
    """
    
    if not filename.endswith('.pdb'):
        raise ValueError('`filename` must be .pdb file')
        
    input_file_path = os.path.join(input_dir_path, filename)
    output_file_path = os.path.join(output_dir_path, filename)
    cleanup_command = ['python', fp.PDB_CLEANUP_SCRIPT_PATH,
                       input_file_path, final_numbering_scheme, output_file_path]
    result_code = subprocess.call(cleanup_command, 
                                  stdout=subprocess.DEVNULL)
        
    status = RESULT_CODE_TO_STATUS_MAPPING.get(result_code, 'other-error')
    
    if status == 'other-error':
        print('Unknown error occured in file {}, process result code {}'.format(
              filename, result_code))
        print('Command:')
        print(' '.join(cleanup_command))
        print('-------')
        
    structure_code = filename.split('.')[0]
    return dict(structure_code=structure_code, status=status)