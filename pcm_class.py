## Main Class to edit the IDF file with PhaseChange material added##
class IDF_EDITING:
    '''
    This Class will take an idf file and does the followings:
    1. Change HeatBalanceAlgorithm to ConductionFiniteDifference from ConductionTransferFunction.
    2. Append a user defined phase change material its and properties stored as pcm_block list to idf file
    3. Add a layer of phasechange material to envelop or roof (once at a time only)
    Inputs: 
        file = path to the idf file to work with [exm: smalloffice.idf]
        _envelope_name = name of the envelop or roof where PCM material layer will be added [exm: 'nonres_ext_envelop_grd']
        _split_word = String for spliting the string to get layer numbers of the layers after PCM added [exm: or '!- Layer ']
        _pcm_layer = The layer where PCM will be added [exm: "!- Layer 3" if added to third layer]

    Outputs:
        create_idf() --> will return the edited idf file with added PCM materials
    Optional Outputs:
        create_idf__no_appending --> will add only a pcm layer adjuscent to wall/roof. It assumes that HBA and PCM 
        properties are already added using create_idf() method.
    '''
    def __init__(self, file, _envelope_name, _split_word, _pcm_layer, _pcm_block, mydict = {}):
        self.file = file
        self._envelope_name = _envelope_name
        self.split_word = _split_word
        self.pcm_layer = _pcm_layer
        self.mydict = mydict
        self.pcm_block = _pcm_block
        

    ## appending pcm properties to idf
    def create_dict_hba(self):
        lines = []
        with open(self.file, 'r') as rf:
            lines = rf.readlines()
        
        ## Changing Heat Balance Alorithm to run PCM in simulation
        for i, line in enumerate(lines):
            if 'ConductionTransferFunction' in line:
                lines[i] = line.replace('ConductionTransferFunction', 'ConductionFiniteDifference')

        lists = lines.copy()

        ## Creating the master dictionary with all items frim idf
        words = {}
        for idx, item in enumerate(lists):
            words[idx] = item.strip()
        
        return words 



    def collect_envelope_const(self):
        words = {}
        words = self.create_dict_hba()
        
        ## Creating a small dictionary only with constructuion set with envelop
        envelope_words = {}
        # _envelope_name = 'nonres_ext_envelop_grd'

        for key, val in words.items():
            if 'Construction' in val:
                # Check if the next line contains 'envelop' in the name
                if key + 1 in words and self._envelope_name in words[key + 1]:
                    current_key = key
                    # Loop and print until a semicolon is found
                    while current_key in words:
                        envelope_words.update({current_key: words[current_key]})
                        if ';' in words[current_key]:
                            break
                        current_key += 1
                    break  # Stop processing after printing the relevant envelop block
        return envelope_words
    


    def add_pcm_construction(self):
        words = {}
        envelope_words = {}

        envelope_words = self.collect_envelope_const()
        words = self.create_dict_hba()

        ## Finding the index of envelop after which PCM will be added
        key_to_pcm = 0
        pos = 0
        items = []
        mydict = {}
  
        for key, val in words.items():
            if 'Construction' in val:
                # Check if the next line contains 'envelop' in the name
                if key + 1 in words and self._envelope_name in words[key + 1]:
                    # PCM layer after 'construction', Name, and then the layer number
                    key_to_pcm = key + 2 + int(self.pcm_layer.split(" ")[-1])
                    break  # Stop processing after printing the relevant envelop block

        ## Creating a new dictionary with adding PCM to desired index
        pos = list(words.keys()).index(key_to_pcm) # Index to where PCM will be added.
        items = list(words.items())
        items.insert(pos, ('Here we go: ', f'PCMBoard,                   {self.pcm_layer}')) ## Inserting PCM to desired index
        mydict = dict(items)

        return pos, mydict # dictionary of idf lines with PCM as construction layer
    


    def updaye_layer_num(self):

        envelope_words = {}
        pos = 0
        mydict = {}

        envelope_words = self.collect_envelope_const()
        pos, mydict = self.add_pcm_construction()

        ## Updating the layer numbers after PCM from intial small envelope_words dictionary
        # for _pcm_layer ! layer 3,counter = 3+1 = 4
        counter =  int(self.pcm_layer.split(" ")[-1]) + 1 
        layer = counter - 1 # ! layer n, n-1

        new_words = {}
        new_val = ""

        for key, val in envelope_words.items():
            if key >= pos:
                # Split the value to isolate the part after '!- Layer '
                parts = val.split(self.split_word)
                if int(parts[1]) >= layer:
                    # Replace the number after "Layer" with the counter
                    new_val = f"{parts[0]}{self.split_word}{counter}"
                    new_words.update({key: new_val})
                    counter += 1  # Increment the counter
                else:
                    # If '!- Layer ' is not found, keep the original value
                    new_val = val
        ## Finally updating the mydict dictionary with envelop_words dictionary with matched key

        for key, val in self.mydict.items():
            if key in new_words:
                self.mydict[key] = new_words[key]  # Update the value for the matching key

        return mydict
    

    ## It will only create idf without appending PCM properties
    def create_idf__no_appending(self):
        idf_final_dict = {}
        idf_final_dict = self.updaye_layer_num()

        file01 = self.file # The idf file to work with
        
        with open(file01, "w") as f:
            for value in idf_final_dict.values():
                f.write(f"{value}\n")  # Write each value on a new line

        return file01
    

    ## It will create full idf if only envelop/roof is asked to change
    def create_idf(self):
        idf_final_dict = {}
        idf_final_dict = self.updaye_layer_num()

        file01 = self.file # The idf file to work with
        
        with open(file01, "w") as f:
            for value in idf_final_dict.values():
                f.write(f"{value}\n")  # Write each value on a new line
            ## Appending these mandatory PCM properties to copied IDF file_path.
        with open(file01, 'a') as f:
            f.write(self.pcm_block)  # Write each value on a new line

        return file01
        


