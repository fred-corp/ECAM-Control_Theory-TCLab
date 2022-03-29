# Lead-Lag
def LeadLag_RT(MV,Kp,Tlag,Tlead,Ts,MVLL,PVInit=0,method='EBD'):
  
  """
  The function "FO_RT" needs to be included in a "for or while loop".
  
  :MV: input vector
  :Kp: process gain
  :Tlag: lag time constant [s]
  :Tlead: lead time constant [s]
  :Ts: sampling period [s]
  :MVLL: output vector
  :PVInit: (optional: default value is 0)
  :method: discretisation method (optional: default value is 'EBD')
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
  • approximationType : list of approximation types for integration and derivation ( looks like : ["EBD", "TRAP"])
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
  
  # Manual mode ?
  if man is True :
    MVi = constrain(manMV[-1], MVmin, MVmax) - MVp - MVd - MV_FF_previous
  else :
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
def IMC_Tuning(K, theta, Tc, T1, T2, T3=0):
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
  Kc = (T1+T2-T3)/((Tc + theta)*K)
  Ti = T1 + T2 - T3
  Td = (T1*T2-(T1 + T2 - T3)*T3)/(T1+T2-T3)

  return Kc,Ti,Td

