# import libraries
import numpy as np
from GetEffDepth import get_eff_depth
import pandas as pd


def rc_section_m_v_design(b, h, rebar_tension, rebar_compression, rebar_v,
                       M, M_qp, Ved, wk, fck, c_nom_comp, c_nom_tens, c_nom_s):
    '''runs bending moment and shear design checks and outputs utilization ratios'''
    '''h # section depth, mm'''
    '''b # section width, mm'''
    '''rebar_tension # example = [[11, 20], [5, 20]]  # this means 1st layer with 11H20 and 2nd layer with 5H20'''
    '''rebar_compression # example  = [[11, 20], ]  # number of [bars,diameter] of bars in compression reinforcement'''
    '''rebar_v = [n_legs, link_d, s_links]  # Shear reinforcement provided, [legs, diameter, spacing] -> [#, mm, mm]'''
    '''M # design bending moment, kN.m'''
    '''M_qp # Quasi-permanent moment, kN.m'''
    '''Ved # Design shear force, kN'''
    '''wk # maximum crack width'''
    '''fck # Characteristic compressive cylinder strength, N/mm2'''
    '''c_nom_comp  # Nominal cover to compression reinforcement, mm'''
    '''c_nom_tens # Nominal cover to tension reinforcement, mm'''
    '''c_nom_s = 35  # Nominal cover to side reinforcement, mm'''


    # import tables
    table7_3N = pd.read_csv('Table_7_3N.csv')



    Ved_max = Ved  # Design shear force at support, kN (assumed same as section in consideration)



    # Concrete details
    AAF = 1.0  # Aggregate adjustment factor - cl.3.1.3(2)

    fcm = fck + 8  # Mean value of compressive cylinder strength, N/mm2
    fctm = 0.3 * (fck) ** (2 / 3)  # Mean value of axial tensile strength, N/mm2
    Ecm = 22000 * (fcm / 10) ** 0.3 * AAF  # Secant modulus of elasticity of concrete, N/mm2
    eps_cu2 = 0.0035  # Ultimate strain - Table 3.1
    eps_cu3 = 0.0035  # Shortening strain - Table 3.1
    lamb = 0.8  # effective compression zone height factor
    nieta = 1  # effective strength factor
    k1 = 0.4  # coefficient k1
    k2 = 1 * (0.6 + 0.0014 / eps_cu2)  # coefficient k2
    k3 = 0.4  # coefficient k3
    k4 = 1 * (0.6 + 0.0014 / eps_cu2)  # coefficient k4
    gamma_c = 1.5  # partial factor for concrete
    alpha_cc = 0.85  # Compressive strength coefficient - cl.3.1.6(1)
    fcd = alpha_cc * fck / gamma_c  # Design compressive concrete strength - exp.3.15, N/mm2
    alpha_ccw = 1.00  # Compressive strength coefficient - cl.3.1.6(1)
    fcwd = alpha_ccw * fck / gamma_c  # Design compressive concrete strength - exp.3.15, N/mm2
    h_agg = 20  # Maximum aggregate size, mm
    rho = 2500  # Density of reinforced concrete, kg/m3
    beta_1 = 0.25  # Monolithic simple support moment factor

    # Reinforcement details
    fyk = 500  # Characteristic yield strength of reinforcement, N/mm2
    gamma_s = 1.15  # Partial factor for reinforcing steel - Table 2.1N
    fyd = fyk / gamma_s  # Design yield strength of reinforcement, N/mm2



    # Fire resistance
    R = 60  # Standard fire resistance period, min
    n_fire = 3  # number of sides exposed to fire
    b_min = 120  # Minimum width of beam - EN1992-1-2 Table 5.5 -> to be developed to get this table automatically

    # Reinforcement check

    d, As_prov = get_eff_depth(rebar_tension, c_nom_tens, rebar_v[1], h)  # Effective depth of tension reinforcement, Area of rebar provided
    delta = 1.00  # redistribution ratio
    K = M / (b * 0.001 * (d * 0.001) ** 2 * fck * 1000)
    Es = 200000  # Design value modulus of elasticity reinf – 3.2.7(4), N/mm2
    K_ = (2 * nieta * alpha_cc / gamma_c) * (1 - lamb * (delta - k1) / (2 * k2)) * (lamb * (delta - k1) / (2 * k2))



    if K_ >= K:
        #print('No compression reinforcement is required.')
        z = min(0.5 * d * (1 + (1 - 2 * K / (nieta * alpha_cc / gamma_c)) ** 0.5), 0.95 * d)  # lever arm, mm
        x = 2 * (d - z) / lamb  # depth of neutral axis
        As_req = M / (fyd * z) * 1e6  # Area of tension reinforcement required, mm2


    else:
        #print('Compression reinforcement required!')
        z = 0.5 * d * (1 + (1 - 2 * K_ / (nieta * alpha_cc / gamma_c)) ** 0.5)  # lever arm, mm
        x = d * (delta - k1) / k2  # depth of neutral axis
        d_comp, As2_prov = get_eff_depth(rebar_compression, c_nom_comp, rebar_v[1],
                                         h)  # Effective depth of compression reinforcement, Area of rebar provided
        d2 = h - d_comp  # Effective depth of compression reinforcement;
        fsc = min(Es * eps_cu3 * (x - d2) / x, fyd)
        As2_req = (K - K_) * fck * b * d ** 2 / (fsc * (d - d2))
        if As2_prov < As2_req:
            print('Area of compression provided (As2_prov)! < Area of compression required (As2_req) ! ')
        As_req = K_ * fck * b * d ** 2 / (fyd * z) + As2_req * fsc / fyd

    As_max = 0.04 * b * h  # Maximum area of reinforcement - cl.9.2.1.1(3)

    As_min = max(0.26 * fctm / fyk, 0.0013) * b * d  # Minimum area of reinforcement - exp.9.1N

    M_ratio1 = np.round(As_min / As_prov, 3)
    M_ratio2 = np.round(As_req / As_prov, 3)

    #print('Moment utilisation: ' + str(M_ratio))

    # Crack control
    Es = 200000  # Design value modulus of elasticity reinf – 3.2.7(4), N/mm2
    fct_eff = fctm  # Mean value of concrete tensile strength, N/mm2
    kc = 0.4  # Stress distribution coefficient
    k = min(max(1 + (300 - min(h, b)) * 0.35 / 500, 0.65), 1)
    s_bar = (b - (2 * (c_nom_s + rebar_v[1]) + rebar_tension[0][1] * rebar_tension[0][0])) / (rebar_tension[0][0] - 1) + \
            rebar_tension[0][1]  # Actual tension bar spacing;
    table7_3N = table7_3N.sort_values(by=['0.3'])  # sort by ascending order of spacing of bars so interpolation works
    sigma_s = np.interp(s_bar, table7_3N[str(wk)], table7_3N['stress'])  # Maximum stress permitted - Table 7.3N
    #print('sigma_s: ', sigma_s)
    alpha_cr = Es / Ecm
    y = (b * h ** 2 / 2 + As_prov * (alpha_cr - 1) * (h - d)) / (
                b * h + As_prov * (alpha_cr - 1))  # Distance of the Elastic NA from tension of beam, mm
    Act = b * y  # Area of concrete in the tensile zone, mm2
    Asc_min = kc * k * fct_eff * Act / sigma_s  # Minimum area of reinforcement required - exp.7.1, mm2

    M_ratio3 = np.round(Asc_min / As_prov, 3)


    if M != 0:
        R_pl = M_qp / M  # Permanent load ratio
        sigma_sr = fyd * As_req / As_prov * R_pl  # Service stress in reinforcement
    else:
        R_pl = 0
        sigma_sr = fyd * As_req / As_prov * R_pl

    table7_3N = table7_3N.sort_values(by=['stress'])  # sort by ascending order of stress so interpolation works
    s_bar_max = np.interp(sigma_sr, table7_3N['stress'], table7_3N[str(wk)])

    M_ratio4 = round(s_bar / s_bar_max, 3)

    M_ratio = max(M_ratio1, M_ratio2, M_ratio3)


    # Section in shear
    teta_max = 45  # Angle of comp. shear strut for maximum shear, degrees
    v1 = 0.6 * (1 - fck / 250)  # Strength reduction factor - cl.6.2.3(3)
    alpha_cw = 1  # Compression chord coefficient - cl.6.2.3(3)
    Asv_min = 0.08 * b * fck ** 0.5 / fyk * 1000  # Minimum area of shear reinforcement - exp.9.5N, mm2/m
    Vrd_max = alpha_cw * b * z * v1 * fcwd / (1 / np.tan(np.radians(teta_max)) + np.tan(
        np.radians(teta_max))) * 0.001  # Maximum design shear resistance - exp.6.9

    ved = Ved * 1000 / (b * z)  # Design shear stress, N/mm2
    teta = min(np.degrees(max(0.5 * np.arcsin(min(2 * ved / (alpha_cw * fcwd * v1), 1)), np.radians(21.8))),
               45)  # Angle of concrete compression strut - cl.6.2.3
    Asv_des = ved * b / (fyd * 1 / np.tan(np.radians(teta))) * 1000  # Area of shear reinforcement required - exp.6.8, mm2/m
    Asv_req = max(Asv_des, Asv_min)  # Area of shear reinforcement required, mm2/m

    Asv_prov = rebar_v[0] * np.pi * rebar_v[1] ** 2 / 4 * 1000 / rebar_v[2]

    V_ratio = np.round(Asv_req / Asv_prov, 3)

    #print('V_ratio = ' + str(V_ratio))

    # Construction details check & Results Summary
    # Bending
    ## ULS
    if As_prov < As_min:
        print('As_prov < As_min!')
        M_ratio = 'As_prov < As_min!'
    if As_prov > As_max:
        print('As_prov > As_max!')
        M_ratio = 'As_prov > As_max!'

    ## SLS
    if As_prov < Asc_min:
        print('As_prov < Asc_min!')
        M_ratio = 'As_prov < Asc_min!'

    if s_bar > s_bar_max:
        print('s_bar > s_bar_max!')
        M_ratio = 's_bar > s_bar_max!'

    #print('Moment ULS utilisation ratio: ' + str(M_ratio))
    #print('Moment SLS utilisation ratio: ' + str(s_bar_ratio))

    # Shear
    if Ved_max > Vrd_max:
        print('Ved_max > Vrd_max at support!')
        V_ratio = 'Ved_max > Vrd_max at support!'

    svl_max = 0.75*d
    if rebar_v[2] > svl_max:
        print('Shear links spacing > Max spacing!')
        V_ratio = 'Shear links spacing > Max spacing!'

    #print('Shear utilization ratio = ' + str(V_ratio))

    return M_ratio, V_ratio

# try function
#ratio = rc_beam_m_v_design(h=800, b=1000, rebar_tension = [[10, 32], ], rebar_compression = [[10, 20], ],
#                                  rebar_v=[5, 12, 250], M = 700.7, M_qp = 509.1, Ved= 805.3, wk = 0.3,
#                                  fck = 30, c_nom_comp = 35 , c_nom_tens = 35, c_nom_s = 35)


