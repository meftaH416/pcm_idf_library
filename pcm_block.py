
class MaterialProperty():
    '''
    This class will create new Materials for energyplus idf and also create PhaseChange property given inputs from users.
    Class Input:
        name = Name of the material to be created [exm: 'PCMBoard']

    Inputs of material(): 
        thickness = Thickness of material layer in meter {m} [exm: 0.025]
        conductivity = thermal conductivity of the materials {W/m-k} [exm: 0.12]
        density = density of material {kg/m3} [exm: 1000]
        specific_heat = specific heat of the material {J/kg-k} [exm: 2100]
        Optional Inputs: 
            roughness,
            ther_abs = thermal absorptance 
            sol_abs = solar absorptance 
            vis_abs = visible absorptance

    Inputs of phasechange():
        temp1 = Temperature 1, C
        enth1 = Enthalpy 1, (J/kg)
        temp2 = Temperature 1, C
        enth2 = Enthalpy 1, (J/kg)
        temp3 = Temperature 1, C
        enth3 = Enthalpy 1, (J/kg)
        temp4 = Temperature 1, C
        enth4 = Enthalpy 1, (J/kg)
        Optional Inputs: 
            temp_coeff = Temperature coefficient, thermal conductivity (W/m K2)
    
    Outputs:
        pcmblock() --> Complete Material along with PhasChange properties as string for idf entry.
        material() --> Any material created by user as string for idf entry.
        phasechange() --> Material property PhaseChange given that PCM material is added first as string for idf entry.

    '''
    def __init__(self, name):
        self.name = name
        self.material_data = None
        self.phasechange_data = None
    
    def material(self, thickness, conductivity, density, specific_heat, roughness='Smooth',
                ther_abs=0.90, sol_abs=0.92, vis_abs=0.92):
        self.material_data = '\n'.join([
            'Material,',
            '    {},                      !- Name'.format(self.name),
            '    {},                      !- Roughness'.format(roughness),
            '    {},                      !- Thickness {{m}}'.format(thickness),
            '    {},                      !- Conductivity {{W/m-K}}'.format(conductivity),
            '    {},                      !- Density {{kg/m3}}'.format(density),
            '    {},                      !- Specific Heat {{J/kg-K}}'.format(specific_heat),
            '    {},                      !- Thermal Absorptance'.format(ther_abs),
            '    {},                      !- Solar Absorptance'.format(sol_abs),
            '    {};                      !- Visible Absorptance'.format(vis_abs),
            '\n'
        ])
        return self.material_data


    def phasechange(self, temp1, enth1, temp2, enth2, temp3, enth3, temp4, enth4, temp_coeff=0.01):
        self.phasechange_data = '\n'.join([
            'MaterialProperty:PhaseChange,',
            '    {},                      !- Name'.format(self.name),
            '    {},                      !- Temperature coefficient, thermal conductivity (W/m K2)'.format(temp_coeff),
            '    {},                      !- Temperature 1, C'.format(temp1),
            '    {},                      !- Enthalpy 1, (J/kg)'.format(enth1),
            '    {},                      !- Temperature 2, C'.format(temp2),
            '    {},                      !- Enthalpy 2, (J/kg)'.format(enth2),
            '    {},                      !- Temperature 3, C'.format(temp3),
            '    {},                      !- Enthalpy 3, (J/kg)'.format(enth3),
            '    {},                      !- Temperature 4, C'.format(temp4),
            '    {};                      !- Enthalpy 4, (J/kg)'.format(enth4),
            '\n'
        ])
        return self.phasechange_data
    

    def pcmblock(self):
        if not self.material_data or not self.phasechange_data:
            raise ValueError("Both material and phase change properties must be set before calling pcmblock.")
        return self.phasechange_data + '\n' + self.material_data



# # Example to use
# pcm_mat = MaterialProperty('pcmboard')
# pcm_mat.material(0.025, 0.27, 1000, 2120)
# pcm_mat.phasechange(-20.0, 0, 23, 55000, 24, 75000, 100, 165000)
# _pcm_block = pcm_mat.pcmblock()