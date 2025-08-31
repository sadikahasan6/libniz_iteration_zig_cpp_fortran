! backend.f90
!
! This module contains a function to calculate Pi using the Leibniz formula
! Can be compiled as a shared library

module backend
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use, intrinsic :: iso_c_binding, only: c_int64_t, c_double
  implicit none
  
contains

  function calculate_pi(iterations) result(pi_value) bind(c, name="calculate_pi")
    ! Calculate Pi using the Leibniz formula
    ! This function is exported for use as a shared library function
    integer(c_int64_t), intent(in), value :: iterations
    real(c_double) :: pi_value
    
    real(dp) :: sum_val, sign_val
    integer(c_int64_t) :: i
    
    sum_val = 0.0_dp
    sign_val = 1.0_dp
    
    do i = 0, iterations - 1
      sum_val = sum_val + sign_val / (2.0_dp * real(i, dp) + 1.0_dp)
      sign_val = -sign_val
    end do
    
    pi_value = 4.0_dp * sum_val
    
  end function calculate_pi

end module backend