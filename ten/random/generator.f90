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




subroutine points_in_sphere_f90(n_points, r_max, r_min, uniform_in_sphere)

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

  uniform_between_radios = (r_max - r_min)* U**(1.0/3.0) + r_min

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
  
end subroutine points_in_sphere_f90




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
     call points_in_sphere_f90(1, epsilon, epsilon, new_position)
     distance = sqrt(sum((new_position + position)**2))

     if (distance <= radio) then
        check = 0
     end if
  end do

  position = position + new_position
  
end subroutine random_walk


! initialize a random seed from the system clock at every run (fortran 95 code)
subroutine init_random_seed(seed)

  INTEGER, intent(IN)                :: seed
  INTEGER                            :: i, n
  INTEGER, DIMENSION(:), ALLOCATABLE :: seeds

  CALL RANDOM_SEED(size = n)
  ALLOCATE(seeds(n))

  ! set the seeds
  seeds = seed + 37 * (/ (i - 1, i = 1, n) /)
  
  CALL RANDOM_SEED(PUT = seeds)

  DEALLOCATE(seeds)

end subroutine init_random_seed
