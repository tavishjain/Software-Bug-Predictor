!-- binary.f90
!-- System-dependent.  Generic skeleton version.
!-- Assumptions about internal representations are unavoidable.
!-- 4 Mar 92, Richard Maine: Version 1.0.

module binary

  !-- The routines in this module deal with conversion of binary data
  !-- between system-dependent internal representations and
  !-- system-independent external representations.  These conversions
  !-- are needed for dealing with reasonably portable binary files,
  !-- specifically the cmp3 and unc3 file formats.  If those formats
  !-- are not implemented, these routines may not be required.

  !-- The system-independent external representations used are:
  !-- Eight-bit ASCII character data.
  !-- Two's complement integers, most significant byte first, in
  !-- 16 and 32-bit sizes.
  !-- Unsigned integers, most significant byte first, in 8 and 24-bit
  !-- sizes.
  !-- IEEE-754 floatting point reals, most significant bits first,
  !-- in 32-bit and 64-bit sizes (plus a special 24-bit size defined
  !-- by truncating the last 8 bits from a 32-bit IEEE real).
  !-- Bit testing and setting for bit-arrays.

  !-- These routines themselves are highly system-dependent.
  !-- To the extent that the internal system representations are
  !-- simillar to the above-described external representations, these
  !-- routines should be relatively easy to implement.  On systems with
  !-- fundamental deviations from the above formats (most notably
  !-- systems not using 8-bit bytes), these routines may be difficult.

  !-- The interface uses assumed-size, rather than asumed-shape buffers.
  !-- The overhead for assumed shape can be unreasonably large here.
  !-- Besides, buffers should always be contiguous.

  !-- This is a generic skeleton version.  It is appropriate for 32-bit
  !-- systems with ieee floatting point, 2s complement integers,
  !-- ASCII characters, high order bytes stored first.
  !-- It uses a 1-byte integer kind i1_kind in the definition of byte_type,
  !-- but any 8-bit type can be substituted.
  !-- It uses a 2-byte integer kind i2_kind for easy sign extension in get_i2.

  !-- 13 Aug 90, Richard Maine.

  use precision

  implicit none
  private

  !-- Byte_type is public with private components.
  type, public :: byte_type
    private
    integer(i1_kind) :: data  !-- Any 8-bit type will do here.
  end type
  type(byte_type), public, parameter :: zero_byte = byte_type(0)

  !-- Public procedures.
  public get_i1, put_i1, get_i2, put_i2, get_i3, put_i3, get_i4, put_i4
  public get_r3, put_r3, get_r4, put_r4, get_r8, put_r8, get_char, put_char
  public copy_bytes, set_bit, test_bit

contains

  subroutine get_i1 (data, data_pos, value)

    !-- Get a 1-byte unsigned integer from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 1.
    integer, intent(out) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = zero_byte
    temp(4) = data(data_pos+1)
    value = transfer(temp,value)
    data_pos = data_pos + 1
    return
  end subroutine get_i1

  subroutine put_i1 (data, data_pos, value)

    !-- Put a 1-byte unsigned integer into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 1.
    integer, intent(in) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = transfer(value,temp)
    data(data_pos+1) = temp(4)
    data_pos = data_pos + 1
    return
  end subroutine put_i1

  subroutine get_i2 (data, data_pos, value)

    !-- Get a 2-byte big endian 2s complement integer from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 2.
    integer, intent(out) :: value

    !-------------------- local.
    type(byte_type) :: temp(2)
    integer(i2_kind) :: temp_i2

    !-------------------- executable code.

    temp = zero_byte
    temp = data(data_pos+1:data_pos+2)
    temp_i2 = transfer(temp,temp_i2)
    value = int(temp_i2, kind=i_kind)
    data_pos = data_pos + 2
    return
  end subroutine get_i2

  subroutine put_i2 (data, data_pos, value)

    !-- Put a 2-byte big endian 2s complement integer into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 2.
    integer, intent(in) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = transfer(value,temp)
    data(data_pos+1:data_pos+2) = temp(3:4)
    data_pos = data_pos + 2
    return
  end subroutine put_i2

  subroutine get_i3 (data, data_pos, value)

    !-- Get a 3-byte big endian unsigned integer from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 3.
    integer, intent(out) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = zero_byte
    temp(2:4) = data(data_pos+1:data_pos+3)
    value = transfer(temp,value)
    data_pos = data_pos + 3
    return
  end subroutine get_i3

  subroutine put_i3 (data, data_pos, value)

    !-- Put a 3-byte big endian unsigned integer into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 3.
    integer, intent(in) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = transfer(value,temp)
    data(data_pos+1:data_pos+3) = temp(2:4)
    data_pos = data_pos + 3
    return
  end subroutine put_i3

  subroutine get_i4 (data, data_pos, value)

    !-- Get a 4-byte big endian 2s complement integer from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 4.
    integer, intent(out) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = data(data_pos+1:data_pos+4)
    value = transfer(temp,value)
    data_pos = data_pos + 4
    return
  end subroutine get_i4

  subroutine put_i4 (data, data_pos, value)

    !-- Put a 4-byte big endian 2s complement integer into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 4.
    integer, intent(in) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = transfer(value,temp)
    data(data_pos+1:data_pos+4) = temp
    data_pos = data_pos + 4
    return
  end subroutine put_i4

  subroutine get_r3 (data, data_pos, value)

    !-- Get a 3-byte big endian ieee real from a byte vector.
    !-- This is a 4-byte ieee real with the last byte truncated.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 3.
    real(r4_kind), intent(out) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp(1:3) = data(data_pos+1:data_pos+3)
    temp(4) = zero_byte
    value = transfer(temp,value)
    data_pos = data_pos + 3
    return
  end subroutine get_r3

  subroutine put_r3 (data, data_pos, value)

    !-- Put a 3-byte big endian ieee real into a byte vector.
    !-- This is a 4-byte ieee real with the last byte truncated.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 3.
    real(r4_kind), intent(in) :: value

    !-------------------- local.
    type(byte_type) :: temp(4)

    !-------------------- executable code.

    temp = transfer(value,temp)
    data(data_pos+1:data_pos+3) = temp(1:3)
    data_pos = data_pos + 3
    return
  end subroutine put_r3

  subroutine get_r4 (data, data_pos, value)

    !-- Get a 4-byte big endian ieee real from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 4.
    real(r_kind), intent(out) :: value
        !-- Value returned.  Note it is a working precision real
        !-- (usually 64 bits) partly so that full ieee single precision
        !-- is always retained, even on non-ieee systems.

    !-------------------- local.
    type(byte_type) :: temp(4)
    real(r4_kind) :: temp_r4

    !-------------------- executable code.

    temp = data(data_pos+1:data_pos+4)
    temp_r4 = transfer(temp, temp_r4)
    value = real(temp_r4, kind=r_kind)
    data_pos = data_pos + 4
    return
  end subroutine get_r4

  subroutine put_r4 (data, data_pos, value)

    !-- Put a 4-byte big endian ieee real into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 4.
    real(r_kind), intent(in) :: value
        !-- Value to be put.  Note it is a working precision real
        !-- (usually 64 bits) partly so that full ieee single precision
        !-- is always retained, even on non-ieee systems.

    !-------------------- local.
    type(byte_type) :: temp(4)
    real(r4_kind) :: temp_r4

    !-------------------- executable code.

    temp_r4 = real(value, kind=r4_kind)
    temp = transfer(temp_r4, temp)
    data(data_pos+1:data_pos+4) = temp
    data_pos = data_pos + 4
    return
  end subroutine put_r4

  subroutine get_r8 (data, data_pos, value)

    !-- Get an 8-byte big endian ieee real from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 8.
    real(r_kind), intent(out) :: value

    !-------------------- local.
    type(byte_type) :: temp(8)

    !-------------------- executable code.

    temp = data(data_pos+1:data_pos+8)
    value = transfer(temp,value)
    data_pos = data_pos + 8
    return
  end subroutine get_r8

  subroutine put_r8 (data, data_pos, value)

    !-- Put an 8-byte big endian ieee real into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.  Returns incremented by 8.
    real(r_kind), intent(in) :: value

    !-------------------- local.
    type(byte_type) :: temp(8)

    !-------------------- executable code.

    temp = transfer(value,temp)
    data(data_pos+1:data_pos+8) = temp
    data_pos = data_pos + 8
    return
  end subroutine put_r8

  subroutine get_char (data, data_pos, string)

    !-- Get an ASCII string from a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.
        !-- Returns incremented by the string length.
    character*(*), intent(out) :: string

    !-------------------- executable code.

    string = transfer(data(data_pos+1:data_pos+len(string)),string)
    data_pos = data_pos + len(string)
    return
  end subroutine get_char

  subroutine put_char (data, data_pos, string)

    !-- Put an ASCII string into a byte vector.
    !-- 21 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(inout) :: data_pos
        !-- Previous byte number in the data.
        !-- Returns incremented by the string length.
    character*(*), intent(in) :: string

    !-------------------- executable code.

    data(data_pos+1:data_pos+len(string)) = transfer(string,data(1:0))
    data_pos = data_pos + len(string)
    return
  end subroutine put_char

  subroutine copy_bytes (source, source_pos, dest, dest_pos, n_bytes)

    !-- Copy bytes from source to destination
    !-- Does not check the byte number ranges.
    !-- 22 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(in) :: source(*)
    integer, intent(inout) :: source_pos
         !-- Used length of source.  Copy starts from source_pos+1.
         !-- Returns incremented by n_bytes.
    type(byte_type), intent(inout) :: dest(*)
    integer, intent(inout) :: dest_pos
         !-- Used length of destination.  Copy starts to dest_pos+1.
         !-- Returns incremented by n_bytes.
    integer, intent(in) :: n_bytes  !-- Number of bytes to copy.

    !-------------------- executable code.

    dest(dest_pos+1:dest_pos+n_bytes) = source(source_pos+1:source_pos+n_bytes)
    source_pos = source_pos + n_bytes
    dest_pos = dest_pos + n_bytes
    return
  end subroutine copy_bytes

  subroutine set_bit (data, bit_num)

    !-- Set a bit in a data vector.
    !-- Probably not the world's most efficient implementation,
    !-- but it should be portable (assuming get_i1 and put_i1 work).
    !-- Per Ansi, we use ibset only for integer types.
    !-- 22 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(in) :: bit_num
      !-- Bit number in the data to be set.
      !-- High order bit of the first byte is numbered 1.

    !-------------------- local.
    integer :: byte_num, byte_bit, i

    !-------------------- executable code.

    byte_num = (bit_num-1)/8       !-- Preceeding byte number for get_i1.
    byte_bit = 7-mod(bit_num-1,8)  !-- Low order bit is numbered 0 for ibset.
    call get_i1(data, byte_num, i)
    i = ibset(i,byte_bit)
    byte_num = byte_num-1
    call put_i1(data, byte_num, i)
    return
  end subroutine set_bit

  function test_bit (data, bit_num)

    !-- Test a bit in a data vector.
    !-- Probably not the world's most efficient implementation,
    !-- but it should be portable (assuming get_i1 works).
    !-- Per Ansi, we use bTest only for integer types.
    !-- 22 Jun 90, Richard Maine.

    !-------------------- interface.
    type(byte_type), intent(inout) :: data(*)
    integer, intent(in) :: bit_num
      !-- Bit number in the data to be tested.
      !-- High order bit of the first byte is numbered 1.
    logical :: test_bit

    !-------------------- local.
    integer :: byte_num, byte_bit, i

    !-------------------- executable code.

    byte_num = (bit_num-1)/8       !-- Preceeding byte number for get_i1.
    byte_bit = 7-mod(bit_num-1,8)  !-- Low order bit is numbered 0 for ibset.
    call get_i1(data, byte_num, i)
    test_bit = btest(i, byte_bit)
    return
  end function test_bit

end module binary
