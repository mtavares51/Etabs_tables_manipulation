import pandas as pd
from RCBeamSectionTorsionDesign_rev1 import rc_section_torsion_design

def rc_beam_torsion_design(beam_forces_df, bottom_rebar, top_rebar, shear_rebar, c_nom_top, c_nom_bot, fck):
    '''runs torsion design check for each station in beam_forces_df dataframe and outputs required additional longitudinal and transverse reinforcement, if needed'''
    '''beam_forces_df: dataframe containing analysis data from beam_forces function output'''
    '''bottom_rebar - list of rebar [[[n, diam],]]] for each beam section - bottom'''
    '''top_rebar - list of rebar [[[n, diam],]]] for each beam section - top'''
    '''shear_rebar - list of shear rebar  [[n_legs, link_d, s_links]] for each section'''
    '''c_nom_top, c_nom_bot, c_nom_s - covers for top, bottom and sides'''
    '''wk - crack width limit'''
    '''fck - concrete compressive strength, MPa'''

    # initialize empty vector to store additional areas
    add_areas = []

    # for each station run section torsion design function
    for i in range(len(beam_forces_df["Station"])):
        # ensure top rebar for hogging moments and bottom rebar for sagging moments
        M_uls = beam_forces_df["M_uls"][i]
        if M_uls >= 0:
            flex_rebar = bottom_rebar[i]
            cover = c_nom_bot

        else:
            flex_rebar = top_rebar[i]
            cover = c_nom_top

        add_areas.append(rc_section_torsion_design(beam_forces_df['b'][i],
                                                   beam_forces_df['h'][i],
                                                   flex_rebar,
                                                   shear_rebar[i],
                                                   beam_forces_df["T"][i],
                                                   beam_forces_df["V"][i],
                                                   fck,
                                                   cover))

    return add_areas


#try function
#add_areas = rc_beam_torsion_design(beam_forces_df, bottom_rebar, top_rebar, shear_rebar, c_nom_top, c_nom_bot, fck)