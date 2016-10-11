subroutine forster_mecha(exiton, aceptors, m, r, traps, n, &
                         r_traps, tau_d, delta_t, np_radio, epsilon, &
                         transfer_traps, transfer_aceptors, transfer_natural, walk)

  !---------------------------------------------------------------------
  !  Mecanismo de transferencia del tipo Forster.
  !
  !  The energy transfer rate constant (k_et) is defined as:
  !  k_et = sum ((1 / tau_d)*(R_0 / r[i]) ** 6)
  !  where r[i] is the distance between the exciton
  !  and each acceptor and R_0 is the Forster radius.
  !  The sum go from 1 to M where M is the number of acceptors.
  !
  !  The radiative transfer rate (k_r) and nonradioactive
  !  transfer rate (k_nr) is defined as
  !  k = k_r + k_nr = 1/tau_d
  !
  !  Then, the probability of the exiton die is
  !  prob_die = 1 - e**(-delta_t * [k_et + k])
  !
  !  The quantum efficiency of transfer is defined as:
  !  psi_et = k_et/(k_et + k)
  !
  ! Parameters
  ! ----------
  ! exiton : double precision, dim(3)
  !     Position of exiton
  ! aceptors : double precision, dim(m, 3)
  !     Positions of all aceptors
  ! m : integer
  !     Number of aceptors
  ! r : double precision
  !     Forster radio of aceptors. [r_forster] = nm.
  ! traps : double precision, dim(3, n)
  !     Positions of all intrinsic aceptors
  ! n : integer
  !     Number of intrinsic aceptors
  ! r_traps : double precision
  !     Forster radioof intrinsic aceptors. [r_forster] = nm.
  ! tau_d : double precision
  !     Lifetime of donor. [tau_D] = ns.
  !
  ! Returns
  ! -------
  ! transfer_traps : double presicion 
  !     Number of total trasnference exiton
  ! transfer_aceptors : double presicion 
  !     Number of total trasnference exiton
  ! transfer_natural : double presicion
  !     Number of total decay exiton
  ! walks : double presicion 
  !     Number of total walks
  !---------------------------------------------------------------------
  implicit none

  integer,                           intent(IN)    :: m, n
  double precision, dimension(3),    intent(INOUT) :: exiton
  double precision, dimension(m, 3), intent(IN)    :: aceptors
  double precision,                  intent(IN)    :: r
  double precision, dimension(n, 3), intent(IN)    :: traps
  double precision,                  intent(IN)    :: r_traps
  double precision,                  intent(IN)    :: tau_d
  double precision,                  intent(IN)    :: delta_t
  double precision,                  intent(IN)    :: np_radio
  double precision,                  intent(IN)    :: epsilon

  integer,                           intent(OUT)   :: transfer_natural
  integer,                           intent(OUT)   :: transfer_traps
  integer,                           intent(OUT)   :: transfer_aceptors
  integer,                           intent(OUT)   :: walk

  double precision :: rate_natural, k_et, rate, rate_intinsic
  double precision :: prob_die, psi_et, psi_intinsic, num1, num2
  integer          :: check

  !---------------------------------------------------------------------
  check = 0

  ! Taza de decaimiento natural
  rate_natural = 1/tau_d

  do while (check == 0)
     ! Taza de decaimiento a los dopantes
     call transfer_rate(exiton, aceptors, m, tau_d, r, rate)
     ! Taza de decaimiento a las trampas
     call transfer_rate(exiton, traps, n, tau_d, &
                        r_traps, rate_intinsic)

     ! Taza de transferencia a cualquier aceptor
     k_et = rate + rate_intinsic

     ! Probabilidad de decaer por cualquier mecanismo
     ! Prob_die = 1 - DEXP(-delta_t * (k_et + k))
     prob_die = 1 - DEXP(-delta_t * (rate + rate_intinsic + rate_natural))

     ! Eficiencia cuantica de transferencia a algun aceptor
     psi_et = rate/(rate_natural + rate + rate_intinsic)
     ! Eficiencia cuantica de transferencia a alguna trampa
     psi_intinsic = rate_intinsic/(rate_natural + rate + rate_intinsic)

     call RANDOM_NUMBER(num1)
     call RANDOM_NUMBER(num2)

     if (prob_die > num1) then
        if (0 < num2 .AND. num2 < psi_et) then
           transfer_aceptors = 1
        else if (psi_et < num2 .AND. num2 < (psi_et + psi_intinsic)) then
           transfer_traps = 1
        else
           transfer_natural = 1
        end if

        check = 1

     else
        call random_walk(exiton, np_radio, epsilon)
        walk = walk + 1
     end if
     
  end do
  
end subroutine forster_mecha




subroutine transfer_rate(exiton, aceptors, m, tau_d, r_forster, rate)

  !---------------------------------------------------------------------
  !  Calculo de la taza de transferencia a los aceptores
  !  intrinsicos o a los agregados.
  !
  ! Parameters
  ! ----------
  ! exiton : like array
  !   Exciton position.
  ! aceptors : like array
  !   Positions of all aceptors.
  ! tau_d : float
  !   Lifetime of donor. [tau_D] = ns.
  ! r_forster : float
  !   Forster radio. [r_forster] = nm.
  !
  ! Returns
  ! -------
  ! rate : float
  !   Rate transference
  !---------------------------------------------------------------------
  implicit none

  integer, intent(IN)                            :: m
  
  double precision, dimension(m, 3), intent(IN)  :: aceptors
  double precision, dimension(3),    intent(IN)  :: exiton
  double precision,                  intent(IN)  :: tau_d, r_forster
  double precision,                  intent(OUT) :: rate

  double precision, dimension(m, 3)              :: square, diff
  double precision, dimension(m)                 :: inverse6, distance_inverse

  double precision                               :: cte
  integer                                        :: j

  !---------------------------------------------------------------------
  cte = r_forster**6/tau_d

  forall(j = 1:m) diff(j, :) = aceptors(j, :) - exiton(:)
  square = diff*diff
  
  distance_inverse = 1/sum(square, dim=2)
  inverse6 = distance_inverse *distance_inverse * distance_inverse
  rate = cte*sum(inverse6, dim=1)
  
end subroutine transfer_rate
