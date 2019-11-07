# Copyright (c) Stanford University
# 
# This source code is patent protected and being made available under the
# terms explained in the ../LICENSE-Academic and ../LICENSE-GOV files.

# Author: Mario J Srouji
# Email: msrouji@stanford.edu

def module_def(module, name, arg_names, arg_signals, num_spaces=2):
    module_definition = " "*num_spaces
    module_definition = module_definition + module + " " + name + " ("

    spaces_so_far = len(module_definition)

    args_length = len(arg_names)
    assert(len(arg_names) == len(arg_signals))

    i = 0
    for arg_name in arg_names:
        module_definition = module_definition + "." + arg_name + "(" + arg_signals[i] + ")"
        if i < args_length - 1:
            module_definition = module_definition + ",\n" + " "*spaces_so_far
        i += 1

    module_definition = module_definition + ");"

    return module_definition

def signal_def(bits, signal_type, signal_name, num_spaces=2):
    if bits == 1:
        return " "*num_spaces + signal_type + " " + signal_name + ";"
    else:
        return " "*num_spaces + signal_type + " [" + str(bits-1) + ":0] " + signal_name + ";"

def module_header(name, inputs, outputs):
    header = "module " + name + " (\n"

    if len(outputs) > 0:
        header = header + "// Outputs\n"

    i = 0
    for out in outputs:
        i += 1
        header = header + out
        if len(inputs) > 0 or i < len(outputs):
            header = header + ",\n"

    if len(inputs) > 0:
        header = header + "// Inputs\n"

    i = 0
    for inp in inputs:
        i += 1
        header = header + inp
        if i < len(inputs):
            header = header + ",\n"

    header = header + ");"

    return header

def module_footer():
    return "endmodule"

def direct_assignment_def(name, expression, num_spaces=2):
    return " "*num_spaces + name + " = " + expression + ";"

def assign_def(name, expression, num_spaces=2):
    return " "*num_spaces + "assign " + name + " = " + expression + ";"

def operator(op, left, right, parens):
    if parens:
        return "(" + left + " " + op + " " + right + ")"
    else:
        return left + " " + op + " " + right

def _equals(left, right, parens=False):
    return operator("==", left, right, parens)

def _and(left, right, parens=False):
    return operator("&&", left, right, parens)

def _or(left, right, parens=False):
    return operator("||", left, right, parens)

def _lt(left, right, parens=False):
    return operator("<", left, right, parens)

def _le(left, right, parens=False):
    return operator("<=", left, right, parens)

def _gt(left, right, parens=False):
    return operator(">", left, right, parens)

def _ge(left, right, parens=False):
    return operator(">=", left, right, parens)

def _constant(bits, value):
    return str(bits) + "'b" + value

def bit_vector(signals):
    vector = "{"
    i = 0
    for signal in signals:
        i += 1
        vector = vector + signal
        if i < len(signals):
            vector = vector + ", "

    vector = vector + "}"

    return vector

def always_def(signal, num_spaces=2):
    return " "*num_spaces + "always @(posedge " + signal + ")"

def always_comb_def(num_spaces=2):
    return " "*num_spaces + "always_comb begin"

def property_def(expression, num_spaces=2):
    return " "*num_spaces + "assume property " + "(" + expression + ");"

def begin(num_spaces=1):
    return " "*num_spaces + "begin"

def end(num_spaces=2):
    return " "*num_spaces + "end"

def inline_conditional(check, true, false, endit):
    inline = check + " ? " + true + " : " + false
    if endit:
        inline = inline + ";"
    return inline

def conditional_header(conditional, expression, num_spaces=2):
    return " "*num_spaces + conditional + " (" + expression + ") begin"

def if_header(expression, num_spaces=2):
    return conditional_header("if", expression, num_spaces=num_spaces)

def else_if_header(expression, num_spaces=2):
    return conditional_header("else if", expression, num_spaces=num_spaces)

def else_header(num_spaces=2):
    return " "*num_spaces + "else begin"

def signal_index(signal, msb, lsb):
    return signal + "[" + msb + ":" + lsb + "]"

def newline(n):
    return "\n"*n


