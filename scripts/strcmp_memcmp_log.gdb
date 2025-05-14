
define record_function_result
  # Check if the current call address is within the desired range
 
  # Record the function call address
  set $call_addr = $pc

  # Start logging to the file
  set logging file /tmp/result.log
  set logging on
  printf "Call address: 0x%x\n", $call_addr

  # Step until the function returns
  finish

  # Get the return value of the function (MIPS uses $v0 for return values)
  set $retval = $v0

  # Print the return value to the log file
  printf "Return value: %d\n\n", $retval

  # Stop logging to the file
  set logging off
 

  # Automatically continue the program regardless of whether logging was done
  continue
end

# Set a breakpoint for strcmp and use the command defined above
break strcmp
commands
  silent
  record_function_result
end

# Continue program execution after setting breakpoints
continue
