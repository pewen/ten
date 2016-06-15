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
