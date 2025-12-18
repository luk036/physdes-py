-- xmake.lua for physdes-cpp
set_project("physdes-cpp")
set_version("0.1.0")

-- Set C++ standard to C++23
set_languages("c++23")

-- Add includes
add_includedirs("include")

-- Library target
target("physdes")
    set_kind("headeronly")
    add_headerfiles("include/(recti/**.hpp)")
    add_includedirs("include", {public = true})

-- Tests
if is_mode("debug") or is_mode("check") then
    target("physdes_tests")
        set_kind("binary")
        add_files("tests/*.cpp")
        add_deps("physdes")
        add_packages("doctest")
        
    -- Add test run
    after_build(function (target)
        os.exec(target:targetfile())
    end)
end

-- Examples
if is_mode("debug") then
    target("example_interval")
        set_kind("binary")
        add_files("src/example_interval.cpp")
        add_deps("physdes")
end

-- Package configuration
package("doctest")
    set_description("The fastest feature-rich C++11/14/17/20/23 single-header testing framework")
    set_homepage("https://github.com/doctest/doctest")
    
    add_urls("https://github.com/doctest/doctest/archive/refs/tags/v2.4.11.tar.gz")
    add_versions("2.4.11", "632ed2c05a7f53fa961381497bf8069093f0d6628c5f26286161fbd32a560186")
    
    on_install(function (package)
        os.cp("doctest/doctest.h", package:installdir("include"))
    end)