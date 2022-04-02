# Lead-Lag
def LeadLag_RT(MV,Kp,Tlag,Tlead,Ts,MVLL,PVInit=0,method='EBD'):
  
  """
  The function "FO_RT" needs to be included in a "for or while loop".
  
  • MV: input vector
  • Kp: process gain
  • Tlag: lag time constant [s]
  • Tlead: lead time constant [s]
  • Ts: sampling period [s]
  • MVLL: output vector
  • PVInit: (optional: default value is 0)
  • method: discretisation method (optional: default value is 'EBD')
    EBD: Euler Backward difference
    EFD: Euler Forward difference
    TRAP: Trapezoïdal method
  
  The function "FO_RT" appends a value to the output vector "PV".
  The appended value is obtained from a recurrent equation that depends on the discretisation method.
  """    
  


  try :
    PV_previous = MVLL[-1]
  except :
    PV_previous = PVInit
    # return PV_previous

  try :
    MV_2 = MV[-2]
  except :
    MV_2 = 0
  
  try :
    MV_1 = MV[-1]
  except :
    MV_1 = 0

  if (Tlag != 0):
    K = Ts/Tlag
    # MV[k+1] is MV[-1] and MV[k] is MV[-2]
    if method == 'EBD':
      MVLLout = (1/(1+K))*PV_previous + (K*Kp/(1+K))*((1+Tlead/Ts)*MV_1-(Tlead/Ts)*MV_2)
    elif method == 'EFD':
      MVLLout = (1-K)*PV_previous + K*Kp*((Tlead/Ts)*MV_1+(1-(Tlead/Ts))*MV_2)
    else:
      MVLLout = (1/(1+K))*PV_previous + (K*Kp/(1+K))*((1+Tlead/Ts)*MV_1-(Tlead/Ts)*MV_2)
  else:
    MVLLout = Kp*MV_1

  MVLL.append(MVLLout)

  #return MVLLout

# Constrain
def constrain(val, min_val, max_val):
  return min(max_val, max(min_val, val))

# PID
def PID_RT(PV, SP, MV, Ts, Kc, Ti, Td, alpha, approximationType, PVinit=0, man=False, manMV=[0], FF_MV=[0], FF_MV_init=0, MVmin=0, MVmax=100):
  """
  parameters : 
  • PV : array of all recorded PV values
  • SP : current SP value
  • MV : dict of all recorded MV ({"MV" : [0], "MVp" : [0], "MVi": [0], "MVd": [0], "E" : [0]})
  • Ts : Sample time (seconds)
  • Kc : PID gain
  • Ti : PID Integration time constant
  • Td : PID Derivation time constant
  • alpha : proportional parameter between Td and Tfd
  • approximationType : list of approximation types for integration and derivation (looks like : ["EBD", "TRAP"]), you can choose EBD or TRAP
  • PVinit : initial PV value (useful for simulations, default = 0)
  • man : boolean, true if manual mode is enabled (default = false)
  • manMV : array of manual MV values (default = [0])
  • FF_MV : array of all Feed-Forward MV values (default = [0])
  • FF_MV_init : initial value for FF_MV (default = 0)
  • MVmin : minimum value of MV (default = 0)
  • MVmax : maximum value of MV (default = 100)
  
  """

  try :
    E = SP - PV[-1]
  except :
    E = SP - PVinit

  try : 
    MVi_previous = MV["MVi"][-1]
  except :
    MVi_previous = 0
  
  try : 
    MVd_previous = MV["MVd"][-1]
  except :
    MVd_previous = 0
  
  try : 
    E_previous = MV["E"][-1]
  except :
    E_previous = 0

  try :
    MV_FF_previous = FF_MV[-1]
  except :
    MV_FF_previous = FF_MV_init

  Tfd = alpha * Td

  # Proportional term
  MVp = Kc * E

  # Intergation term
  if approximationType[0] == "TRAP":
    MVi = MVi_previous + ((Kc*Ts)/(2*Ti)) * (E + E_previous)
  elif approximationType[0] == "EBD":
    MVi = MVi_previous + ((Kc*Ts)/Ti) * E

  # Derivative term
  if approximationType[1] == "TRAP":
    MVd = ((Tfd-(Ts/2))/(Tfd+(Ts/2))) * MVd_previous + ((Kc*Td)/(Tfd+(Ts/2))) * (E - E_previous)
  elif approximationType[1] == "EBD":
    MVd = (Tfd/(Tfd+Ts)) * MVd_previous + ((Kc*Td)/(Tfd+Ts)) * (E - E_previous)
  
  # Manual PID mode ?
  if man is True :
    MVi = constrain(manMV[-1], MVmin, MVmax) - MVp - MVd
  
  if (MVp + MVi + MVd + MV_FF_previous) > MVmax :
    MVi = MVmax - MVp - MVd - MV_FF_previous
  if (MVp + MVi + MVd + MV_FF_previous) < MVmin :
    MVi = MVmin - MVp - MVd - MV_FF_previous

  # Calculate MV
  _MV = MVp + MVi + MVd + MV_FF_previous

  MV["MV"].append(_MV)
  MV["MVp"].append(MVp)
  MV["MVi"].append(MVi)
  MV["MVd"].append(MVd)
  MV["E"].append(E)

  #output = {"MV": MV, "MVp": MVp, "MVi": MVi, "MVd": MVd, "E": E}
  #return output

# IMC Tuning
def IMC_Tuning(K, theta, Tc, T1, T2, T3=0, method='FOPDT'):
    """
    parameters :
    • K : Kp => process gain
    • theta : theta p => process offset
    • Tc : Controller time constant
    • T1 : processus first time constant
    • T2 : processus second time constant
    • T3 : processus third time constant

    returns Kc, Ti, Td
    """
    #IMC_Tuning only for an I case (check slide 186/224 of the course)
    if method == 'SOPDT':
        Kc = (T1+T2-T3)/((Tc + theta)*K)
        Ti = T1 + T2 - T3
        Td = (T1*T2-(T1 + T2 - T3)*T3)/(T1+T2-T3)
        
    #IMC_Tuning only for a case where T2p << T1p(check slide 186/224 of the course)
    elif method == 'FOPDT':
        #This is a G case
        Kc = T1/((Tc+theta)*K)
        Ti = T1
        Td = 0
        #This is a H case
        #Kc = (T1+(theta/2))/((Tc+theta/2)*K)
        #Ti = T1 + theta/2
        #Td = (T1*theta)/(2*T1+theta)

    return Kc,Ti,Td


import matplotlib.pyplot as plt
import numpy as np

class Controller:
    
  def __init__(self, parameters):
      
    self.parameters = parameters
    self.parameters['Kc'] = parameters['Kc'] if 'Kc' in parameters else 1.0
    self.parameters['Ti'] = parameters['Ti'] if 'Ti' in parameters else 0.0
    self.parameters['Td'] = parameters['Td'] if 'Td' in parameters else 0.0
    self.parameters['alpha'] = parameters['alpha'] if 'alpha' in parameters else 0.0

def Margins(P, C,omega, Show = True):
  
  """
  • P: Process as defined by the class "Process".
    Use the following command to define the default process which is simply a unit gain process:
      P = Process({})
    
    A delay, two lead time constants and 2 lag constants can be added.
    
    Use the following commands for a SOPDT process:
      P.parameters['Kp'] = 1.1
      P.parameters['Tlag1'] = 10.0
      P.parameters['Tlag2'] = 2.0
      P.parameters['theta'] = 2.0
    
    Use the following commands for a unit gain Lead-lag process:
      P.parameters['Tlag1'] = 10.0        
      P.parameters['Tlead1'] = 15.0        
    
  • C: Process as defined by the class "Controller".
    Use the following command to define the default controller:
      C = Controller({})
    Use the following commands for a PID process:
      C.parameters['Kc'] = 1.1
      C.parameters['Ti'] = 10.0
      C.parameters['Td'] = 2.0
      C.parameters['alpha'] = 2.0 
    
  • omega: frequency vector (rad/s); generated by a command of the type "omega = np.logspace(-2, 2, 10000)".
  • Show: boolean value (optional: default value = True). If Show = True, the Bode diagram is shown. Otherwise Ps (P(j omega)) (vector of complex numbers) is returned.
  
  The function "Bode" generates the Bode diagram of the system with calculated phase margins.
  """     
  
  s = 1j*omega
  
  # Create params for P
  Ptheta = np.exp(-P.parameters['theta']*s)
  PGain = P.parameters['Kp']*np.ones_like(Ptheta)
  PLag1 = 1/(P.parameters['Tlag1']*s + 1)
  PLag2 = 1/(P.parameters['Tlag2']*s + 1)
  PLead1 = P.parameters['Tlead1']*s + 1
  PLead2 = P.parameters['Tlead2']*s + 1
  
  Ps = np.multiply(Ptheta,PGain)
  Ps = np.multiply(Ps,PLag1)
  Ps = np.multiply(Ps,PLag2)
  Ps = np.multiply(Ps,PLead1)
  Ps = np.multiply(Ps,PLead2)

  # Create params for C
  Cs = C.parameters['Kc']*(1 + (1/C.parameters['Ti'])*s + (C.parameters['Td']*s)/(C.parameters['alpha'] * C.parameters['Td'] * s + 1))

  # Calculate values for Bode diagram of L=P*C
  Ls = np.multiply(Ps,Cs)
  
  
  if Show == True:
  
    fig, (ax_gain, ax_phase) = plt.subplots(2,1)
    fig.set_figheight(12)
    fig.set_figwidth(22)

    gain = 20*np.log10(np.abs(Ls))
    phase = (180/np.pi)*np.unwrap(np.angle(Ls))

    # find index of gain where gain is close to 0
    idx_gain_zero = np.argmin(np.abs(gain))

    # find index of phase where phase is close to -180
    idx_phase_neg180 = np.argmin(np.abs(phase - (-180)))
    
    # find x values for gain and phase margins
    gainCross = omega[idx_gain_zero]
    phaseCross = omega[idx_phase_neg180]

    # Plot Bode diagram

    ax_gain.set_title('Bode plot of L(s), with phase margin of {}°, and gain margin of {} dB'.format(np.around(180+phase[idx_gain_zero], decimals=3), np.around(-gain[idx_phase_neg180], decimals=3)))

    # Gain part

    # Gain margin line
    point1 = [phaseCross, gain[idx_phase_neg180]]
    point2 = [phaseCross, 0]
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    ax_gain.plot(x_values, y_values, label='Gain margin')

    ax_gain.semilogx(omega,gain,label='L(s)')
    ax_gain.axhline(y=0, color='r', linestyle='-', label='0 dB')
    gain_min = np.min(20*np.log10(np.abs(Ls)/5))
    gain_max = np.max(20*np.log10(np.abs(Ls)*5))
    ax_gain.set_xlim([np.min(omega), np.max(omega)])
    ax_gain.set_ylim([gain_min, gain_max])
    ax_gain.set_ylabel('Amplitude |L| [db]')
    ax_gain.legend(loc='best')
  
    # Phase part

    # Phase margin line
    point1 = [gainCross, -180]
    point2 = [gainCross, phase[idx_gain_zero]]
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    ax_phase.plot(x_values, y_values, label='Phase margin')

    ax_phase.semilogx(omega, phase, label='L(s)') 
    ax_phase.axhline(y=-180, color='r', linestyle='-', label='-180 deg')
    ax_phase.set_xlim([np.min(omega), np.max(omega)])
    ph_min = np.min((180/np.pi)*np.unwrap(np.angle(Ls))) - 10
    ph_max = np.max((180/np.pi)*np.unwrap(np.angle(Ls))) + 10
    ax_phase.set_ylim([np.max([ph_min, -200]), ph_max])
    ax_phase.set_ylabel(r'Phase $\angle L$ [°]')
    ax_phase.legend(loc='best')
  else:
    return Ls