cmake_minimum_required(VERSION 3.21)

project(dynasm_headers)


add_library(Dynasm INTERFACE)
target_include_directories(Dynasm INTERFACE ../dynasm/)