# import libraries
import numpy as np
import pandas as pd
from GetEffDepth import get_eff_depth


def rc_section_torsion_design(b, h, flex_rebar, rebar_v, Ted, Ved, fck, cover):
    '''runs torsion design checks and outputs required additional longitudinal and transverse reinforcement'''
    '''h # section depth, mm'''
    '''b # section width, mm'''
    '''flex_rebar # example = [[11, 20], [5, 20]]  # this means 1st layer with 11H20 and 2nd layer with 5H20'''
    '''rebar_v = [n_legs, link_d, s_links]  # Shear reinforcement provided, [legs, diameter, spacing] -> [#, mm, mm]'''
    '''Ted # torsion design load'''
    '''Ved # shear design load'''
    '''fck # Characteristic compressive cylinder strength, N/mm2'''
    '''cover  # Nominal cover to flex_rebar, mm'''

    # Concrete details
    gamma_c = 1.5  # partial factor for concrete
    alpha_cw = 1.00  # Compressive chord strength coefficient - cl.6.2.3(3)
    alpha_cc = 0.85  # Compressive strength coefficient - cl.3.1.6(1)
    fcd = alpha_cc*fck/gamma_c  # Design compressive concrete strength - exp.3.15, N/mm2
    alpha_ccw = 1.00  # Compressive strength coefficient - cl.3.1.6(1)
    fcwd = alpha_ccw*fck/gamma_c  # Design compressive concrete strength - exp.3.15, N/mm2
    alpha_ct = 1.00  # tensile strenght coefficient - cl. 3.1.6(2)
    fctm = 0.3*(fck)**(2/3)  # Mean value of axial tensile strength, N/mm2 - cl. 3.1.6(2)
    fctk_005 = 0.7*fctm  # Characteristic axial strength of conc. (5% factile)
    fct_d = alpha_ct*fctk_005/gamma_c  # Design axial strength of concrete


    # Reinforcement details
    fyk = 500  # Characteristic yield strength of reinforcement, N/mm2
    gamma_s = 1.15  # Partial factor for reinforcing steel - Table 2.1N
    fyd = fyk / gamma_s  # Design yield strength of reinforcement, N/mm2


    # Design forces
    d1, Asl = get_eff_depth(flex_rebar, cover, rebar_v[1], h)   # Get As - Area of rebar provided


    # effective depth calc
    d = h - cover - rebar_v[1] - flex_rebar[0][1]/2  # effective depth to outer layer

    # torsional resistance - Section 6.3
    tef_i = (b * h) / (2 * (b + h))  # Effective thickness of walls, mm - cl.6.3.2(1)
    Ak = (b - tef_i) * (h - tef_i)  # Area enclosed by centre lines of walls, mm - cl.6.3.2(1)
    Uk = 2 * ((b - tef_i) + (h - tef_i))  # Perimeter, mm - cl.6.3.2(3);
    v1 = 0.6 * (1 - fck / 250)  # Strength reduction factor;
    vt_ed = Ved / (b*d) * 1000 # Design shear stress, N/mm2;
    tau_t_ed = Ted * 1000000 / (2 * Ak * tef_i)  # Torsional shear stress in wall, N/mm2 - exp.6.26;
    teta_user = 45  # User defined concrete strut angle, degrees;
    teta_t = min(max(teta_user, 21.8), 45)  # Concrete strut angle, degrees;
    T_Rd_max = 2 * v1 * alpha_cw * fcd * Ak * tef_i * np.sin(np.radians(teta_t)) * np.cos(np.radians(teta_t)) * 0.000001 # Max design value of torsional resist. mnt - exp 6.30
    V_Rdt_max = alpha_cw * b * 0.9 * d * v1 * fcwd / ((1/np.tan(np.radians(teta_t))) + np.tan(np.radians(teta_t))) * 0.001 #  Max design shear force - exp.6.9
    interaction_ratio_T = Ted / T_Rd_max + Ved/V_Rdt_max  # Interaction formulae - exp.6.29;


    # Torsional and shear resistance of the concrete alone
    T_Rd_c = 2 * Ak * fct_d * tef_i * 0.000001 # Max torsional resist mnt no shear reinf., kNm - cl.6.3.2(5)
    C_Rd_c = 0.18 / gamma_c  # Shear resistance constant - cl.6.2.2
    rho_l = min(Asl / (d * b), 0.02)  # Reinforcement ratio - cl.6.2.2;
    kv = min(1 + (200 / d)**(1/2), 2)  # Effective depth factor - cl.6.2.2
    v_min = 0.035 * kv**(3/2) * fck**0.5  # Minimum shear stress, N/mm2
    V_Rd_c = max(C_Rd_c * kv * (100* rho_l * fck)**(1/3) * b * d, v_min * b * d) * 0.001  # Design value for shear resistance - exp.6.2.a
    interaction_ratio_T_V = Ted / T_Rd_c + Ved / V_Rd_c  # Interaction formulae - exp.6.31


    # Required torsional reinforcement
    Asl_req = Ted * Uk * (1/np.tan(np.radians(teta_t)))  / (2 * Ak * fyd) * 1000000  # Required area of add. long. reinf. for torsion, mm2
    Asl_req = np.round(Asl_req, 0)
    # The longitudinal bars should be arranged so there is at least one bar at each corner with the other spaced around the
    # periphery of the links at a spacing of 350mm or less (cl.9.2.3(4))

    Asw_req = Ted / (2 * Ak * fyd * (1/np.tan(np.radians(teta_t)))) * 1000000000  # Required shear reinforcement for torsion (one leg), mm2/m
    Asw_req = np.round(Asw_req, 0)
    sw_max = min(Uk/8, b, h)  # Maximum spacing for torsion shear reinforcement

    if interaction_ratio_T_V <= 1:
        Asl_req = ''
        Asw_req = ''

    return Asl_req, Asw_req


# try function
#Asl, Asw = rc_section_torsion_design(1000, 800, [[10,32]], [5,12,250], 150, 750, 30, 35)









