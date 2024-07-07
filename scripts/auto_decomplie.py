import idaapi
import idautils
import idc
import ida_bytes

# 目标函数的名称
target_function_name = "sub_171EC"
base_address = idaapi.get_imagebase()

# 获取目标函数的地址
function_address = idc.get_name_ea_simple(target_function_name)

if function_address == idc.BADADDR:
    print("Target function not found.")
else:
    # 查找所有对目标函数的调用
    for ref in idautils.CodeRefsTo(function_address, False):
        print(f"Found call at address: {hex(ref)}")

        # 向上检查指令以获取LDR参数
        prev_inst = ref
        ldr_instrs = []

        # 从调用点向上寻找LDR指令
        while len(ldr_instrs) < 3:
            prev_inst = idc.prev_head(prev_inst)
            if idc.print_insn_mnem(prev_inst) == 'LDR':
                ldr_instrs.append(prev_inst)
                if len(ldr_instrs) == 3:
                    break

        if len(ldr_instrs) < 3:
            print(f"Not enough LDR instructions found at {hex(ref)}")
            continue
        
        res_array = []
        first_arg_ldr = ldr_instrs[2]
        first_arg_value = idc.get_operand_value(first_arg_ldr, 1)
        res_array.append(first_arg_value)
        second_arg_ldr = ldr_instrs[1]
        second_arg_value = idc.get_operand_value(second_arg_ldr, 1) 
        res_array.append(second_arg_value)
        third_arg_ldr = ldr_instrs[0]
        third_arg_value = idc.get_operand_value(third_arg_ldr, 1) 
        res_array.append(third_arg_value)
        res_array.remove(min(res_array))

        value_array = []
        for item in res_array:
            value_array.append(ida_bytes.get_dword(item) + 0xFF3B8)


        url = ""
        function_addr = None

        if idc.get_strlit_contents(value_array[0], -1, idc.STRTYPE_C):
            url = idc.get_strlit_contents(value_array[0], -1, idc.STRTYPE_C)
            function_addr = ida_bytes.get_dword(value_array[1])
        else:
            url = idc.get_strlit_contents(value_array[1], -1, idc.STRTYPE_C)
            function_addr = ida_bytes.get_dword(value_array[0])

        print(url, function_addr)
        url = url.decode('utf-8')
        decompiled_func = idaapi.decompile(function_addr)
        if decompiled_func:
            # 将函数的反编译代码转换为字符串
            decompiled_code = str(decompiled_func)

            # 文件名使用第二个参数命名，添加.txt后缀
            filename = f"data/{url}.txt"

            # 保存到文件
            with open(filename, "w") as f:
                f.write(f"First Argument: {url}\n\n")
                f.write(decompiled_code)
                print(f"Decompiled code has been saved to {filename}.")
        else:
            print(f"Failed to decompile function {second_arg_str} at {hex(second_func_address)}.")
