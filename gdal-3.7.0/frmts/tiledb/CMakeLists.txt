add_gdal_driver(TARGET gdal_TileDB SOURCES tiledbcommon.cpp tiledbdense.cpp tiledbsparse.cpp PLUGIN_CAPABLE)
gdal_standard_includes(gdal_TileDB)
target_compile_definitions(gdal_TileDB PRIVATE -DTILEDB_DEPRECATED=)
target_compile_features(gdal_TileDB PRIVATE cxx_std_17)
gdal_target_link_libraries(gdal_TileDB PRIVATE TileDB::tiledb_shared)
