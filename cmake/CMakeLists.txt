cmake_minimum_required(VERSION 3.21)

project(dynasm_headers)

add_library(Dynasm INTERFACE ../dynasm/dasm_arm.h ../dynasm/dasm_mips.h ../dynasm/dasm_ppc.h ../dynasm/dasm_proto.h ../dynasm/dasm_x86.h )