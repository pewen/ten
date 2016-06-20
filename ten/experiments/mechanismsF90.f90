subroutine transfer_rate (exiton, aceptors, m, tau_d, r_forster, rate)

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



subroutine Fors(exiton, aceptors, m, r, intrinsic_aceptors, n, r_intrinsic, &
                   tau_d, delta_t, np_radio, epsilon, transfer, decay, walk)

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
  ! intrinsic_aceptors : double precision, dim(3, n)
  !     Positions of all intrinsic aceptors
  ! n : integer
  !     Number of intrinsic aceptors
  ! r_intrinsic : double precision
  !     Forster radioof intrinsic aceptors. [r_forster] = nm.
  ! tau_d : double precision
  !     Lifetime of donor. [tau_D] = ns.
  !
  ! Returns
  ! -------
  ! transf : double presicion 
  !     Number of total trasnference exiton
  ! decay : double presicion
  !     Number of total decay exiton
  ! walks : double presicion 
  !     Number of total walks
  !---------------------------------------------------------------------
  implicit none

  integer, intent(IN) :: m, n
  double precision, dimension(3),    intent(INOUT) :: exiton
  double precision, dimension(m, 3), intent(IN) :: aceptors
  double precision,                  intent(IN) :: r
  double precision, dimension(n, 3), intent(IN) :: intrinsic_aceptors
  double precision,                  intent(IN) :: r_intrinsic
  double precision,                  intent(IN) :: tau_d
  double precision,                  intent(IN) :: delta_t
  double precision,                  intent(IN) :: np_radio
  double precision,                  intent(IN) :: epsilon

  integer, intent(OUT)                          :: decay
  integer, intent(OUT)                          :: transfer
  integer, intent(OUT)                          :: walk

  double precision :: k, k_et, rate, rate_intinsic, prob_die, psi_et, num1,num2
  integer :: check

  !---------------------------------------------------------------------
  check = 0

  k = 1/tau_d

  do while (check == 0)
     call transfer_rate(exiton, aceptors, m, tau_d, r, rate)
     call transfer_rate(exiton, intrinsic_aceptors, n, tau_d, &
          r_intrinsic, rate_intinsic)

     ! Taza de transferencia a cualquier aceptor
     k_et = rate + rate_intinsic

     ! Probabilidad de decaer por cualquier mecanismo
     prob_die = 1 - DEXP(-delta_t * (k_et + k))

     ! Eficiencia cuantica de transferencia
     psi_et = k_et/(k_et + k)

     call RANDOM_NUMBER(num1)
     call RANDOM_NUMBER(num2)

     if (prob_die > num1) then
        if (psi_et < num2) then
           decay = decay + 1
        else
           transfer = transfer + 1
        end if
        check = 1
     else
        call random_walk(exiton, np_radio, epsilon)
        walk = walk + 1
     end if
     
  end do
  
end subroutine Fors










function random_normal()

  !---------------------------------------------------------------------
  ! Adapted from the following Fortran 77 code
  !      ALGORITHM 712, COLLECTED ALGORITHMS FROM ACM.
  !      THIS WORK PUBLISHED IN TRANSACTIONS ON MATHEMATICAL SOFTWARE,
  !      VOL. 18, NO. 4, DECEMBER, 1992, PP. 434-435.
  !
  !  The function random_normal() returns a normally distributed pseudo-random
  !  number with zero mean and unit variance.
  !
  !  The algorithm uses the ratio of uniforms method of A.J. Kinderman
  !  and J.F. Monahan augmented with quadratic bounding curves.
  !---------------------------------------------------------------------
  
  IMPLICIT NONE

  double precision :: random_normal
  REAl :: half = 0.5
  REAL :: s = 0.449871, t = -0.386595, a = 0.19600, b = 0.25472
  REAL :: r1 = 0.27597, r2 = 0.27846, u, v, x, y, q
  !---------------------------------------------------------------------
  
  ! Generate P = (u,v) uniform in rectangle enclosing acceptance region
  DO
     CALL RANDOM_NUMBER(u)
     CALL RANDOM_NUMBER(v)
     v = 1.7156 * (v - half)

     ! Evaluate the quadratic form
     x = u - s
     y = ABS(v) - t
     q = x**2 + y*(a*y - b*x)

     ! Accept P if inside inner ellipse
     IF (q < r1) EXIT
     ! Reject P if outside outer ellipse
     IF (q > r2) CYCLE
     ! Reject P if outside acceptance region
     IF (v**2 < -4.0*LOG(u)*u**2) EXIT
  END DO

  ! Return ratio of P's coordinates as the normal deviate
  random_normal = v/u

  RETURN

END function  random_normal




subroutine points_in_sphere(n_points, r_max, r_min, uniform_in_sphere)

  !---------------------------------------------------------------------
  !  Return a array with the cordenades in cartesian for a
  !  point between two sphere of radio_out and radio_in.
  !  If R == r points are in the surface
  !
  !  Parameters
  !  ----------
  !  n_points = int
  !      Number of points in sphere
  !  R : float
  !      Radio max of generate
  !  r : floar
  !      Radio min of generate. Default "0"
  !
  !  Is not trivial generate random point in a sphere.
  !  See the ipython notebook in:
  !  ten/IPython_notebooks/Random_points_in_sphere.ipynb
  !  to understan why we generate for this form.
  !---------------------------------------------------------------------

  implicit none

  integer,                                  intent(IN)  :: n_points
  double precision,                         intent(IN)  :: r_max
  double precision,                         intent(IN)  :: r_min
  double precision, dimension(n_points, 3), intent(OUT) :: uniform_in_sphere
  
  double precision, dimension(3, n_points) :: pointsT, versors, trans
  double precision, dimension(n_points, 3) :: X
  double precision, dimension(n_points)    :: U, uniform_between_radios, a

  double precision :: random_normal
  integer ::i, j


  !---------------------------------------------------------------------
  !CALL RANDOM_SEED()
  CALL RANDOM_NUMBER(U)

  uniform_between_radios = (r_max - r_min)* U**(1/3) + r_min

  do i = 1, 3
     do j = 1, n_points
        X(j, i) = random_normal()
     end do
  end do

  trans = TRANSPOSE(X)
  a = sqrt(sum(X**2, dim=2))**(-1)
  forall(j=1:3) versors(j, :) = trans(j, :) * a

  forall(j=1:3) pointsT(j, :) = versors(j, :) * uniform_between_radios

  uniform_in_sphere = TRANSPOSE(pointsT)
  
end subroutine points_in_sphere




subroutine random_walk(position, radio, epsilon)

  !---------------------------------------------------------------------
  ! Exciton make a random walk inside the nanoparticle.
  ! The size of the walk is fixed (epsilon).
  !
  ! Parameters
  ! ----------
  ! exiton_position : array, dim(3)
  !
  !---------------------------------------------------------------------
  implicit none

  double precision, dimension(3), intent(INOUT)  :: position
  double precision,               intent(IN)     :: radio
  double precision,               intent(IN)     :: epsilon

  
  double precision, dimension(3)              :: new_position
  double precision                            :: distance
  integer                                     :: check
  
  !---------------------------------------------------------------------
  check = 1

  do while (check == 1)
     call points_in_sphere(1, epsilon, epsilon, new_position)
     distance = sqrt(sum((new_position + position)**2))

     if (distance <= radio) then
        check = 0
     end if
  end do

  position = position + new_position
  
end subroutine random_walk
