import numpy as np


from RCBeamSectionMandVdesign_rev2 import rc_section_m_v_design

def rc_beam_M_V_design(beam_forces_df, bottom_rebar, top_rebar, shear_rebar, c_nom_top, c_nom_bot, c_nom_s, wk, fck):
    '''runs bending moment and shear design checks for each station in beam_forces_df dataframe and outputs ratios'''
    '''beam_forces_df: dataframe containing analysis data from beam_forces function output'''
    '''bottom_rebar - list of rebar [[[n, diam],]]] for each beam section - bottom'''
    '''top_rebar - list of rebar [[[n, diam],]]] for each beam section - top'''
    '''shear_rebar - list of shear rebar  [[n_legs, link_d, s_links]] for each section'''
    '''c_nom_top, c_nom_bot, c_nom_s - covers for top, bottom and sides'''
    '''wk - crack width limit'''
    '''fck - concrete compressive strength, MPa'''


    # initialize empty vector to store ratios and bar spacings
    ratios = []
    s_bar_top = [''] * len(beam_forces_df["Station"])
    s_bar_bottom = [''] * len(beam_forces_df["Station"])

    # for each station run section beam design function
    for i in range(len(beam_forces_df["Station"])):

        # ensure top rebar for hogging moments and bottom rebar for sagging moments
        M_uls = beam_forces_df["M_uls"][i]
        M_sls = abs(beam_forces_df["M_sls"][i])
        if M_uls >= 0:
            tension_rebar = bottom_rebar[i]
            compression_rebar = top_rebar[i]
            c_nom_comp = c_nom_top
            c_nom_tens = c_nom_bot
        else:
            tension_rebar = top_rebar[i]
            compression_rebar = bottom_rebar[i]
            c_nom_tens = c_nom_top
            c_nom_comp = c_nom_bot
            M_uls = abs(M_uls)  # design function doesn't work with negative signal for bending moment
            M_sls = abs(M_sls)  # design function doesn't work with negative signal for bending moment

        ratios.append(rc_section_m_v_design(beam_forces_df['b'][i],
                                        beam_forces_df['h'][i],
                                        tension_rebar,
                                        compression_rebar,
                                        shear_rebar[i],
                                        M_uls,
                                        M_sls,
                                        beam_forces_df['V'][i],
                                        wk,
                                        fck,
                                        c_nom_tens,
                                        c_nom_comp,
                                        c_nom_s)
                      )



        s_bar_top[i] = (beam_forces_df['b'][i] - (2 * (c_nom_s + shear_rebar[i][1]) + top_rebar[i][0][1] *
                                                    top_rebar[i][0][0])) / (top_rebar[i][0][0] - 1)
        s_bar_bottom[i] = (beam_forces_df['b'][i] - (2 * (c_nom_s + shear_rebar[i][1]) + bottom_rebar[i][0][1] *
                                                    bottom_rebar[i][0][0])) / (bottom_rebar[i][0][0] - 1)

    s_bar_top = np.asarray(s_bar_top)
    s_bar_bottom = np.asarray(s_bar_bottom)
    s_bar_top = np.round(s_bar_top, 1)
    s_bar_bottom = np.round(s_bar_bottom, 1)

    return ratios, s_bar_top, s_bar_bottom

