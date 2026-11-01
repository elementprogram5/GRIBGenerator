from __future__ import annotations
from dataclasses import dataclass
from .base import ProductDefinitionTemplate
from grib.utils import (uint1, uint2, uint4, sint4)
from enum import IntEnum

class StatisticalProcess(IntEnum):
    AVERAGE = 0
    ACCUMULATION = 1
    MAXIMUM = 2
    MINIMUM = 3
    DIFFERENCE = 4
    RMS = 5
    STANDARD_DEVIATION = 6

class EnsembleForecastType(IntEnum):
    UNPERTURBED_HIGH_RESOLUTION = 0
    UNPERTURBED_LOW_RESOLUTION = 1
    NEGATIVELY_PERTURBED = 2
    POSITIVELY_PERTURBED = 3

class DerivedForecastType(IntEnum):
    UNWEIGHTED_MEAN = 0
    WEIGHTED_MEAN = 1
    STANDARD_DEVIATION = 2
    STANDARDIZED_ANOMALY = 3
    CLUSTER_MEAN = 4
    MINIMUM = 5
    MAXIMUM = 6
    SPREAD = 7

class SpatialStatisticalProcess(IntEnum):
    AVERAGE = 0
    ACCUMULATION = 1
    MAXIMUM = 2
    MINIMUM = 3
    DIFFERENCE = 4
    RMS = 5
    STANDARD_DEVIATION = 6

class SpatialProcessingType(IntEnum):
    RECTANGULAR = 0
    CIRCULAR = 1
    ELLIPTICAL = 2


def encode_template40_fields(self) -> bytearray:
    data = bytearray()
    # Octet 1
    data.extend(uint1(self.parameter_category))
    # Octet 2
    data.extend(uint1(self.parameter_number))
    # Octet 3
    data.extend(uint1(self.generating_process_type))
    # Octet 4
    data.extend(uint1(self.background_process_id))
    # Octet 5
    data.extend(uint1(self.generating_process_id))
    # Octets 6-7
    data.extend(uint2(self.hours_after_reference))
    # Octet 8
    data.extend(uint1(self.minutes_after_reference))
    # Octet 9
    data.extend(uint1(self.forecast_time_unit))
    # Octets 10-13
    data.extend(sint4(self.forecast_time))
    # Octet 14
    data.extend(uint1(self.surface_type))
    # Octet 15
    data.extend(uint1(self.surface_scale_factor))
    # Octets 16-19
    data.extend(uint4(self.surface_value))
    # Octet 20
    data.extend(uint1(self.second_surface_type))
    # Octet 21
    data.extend(uint1(self.second_surface_scale_factor))
    # Octets 22-25
    data.extend(uint4(self.second_surface_value))
    return data

def encode_ensemble_fields(self, data: bytearray):
    # Octet 26
    data.extend(uint1(self.ensemble_type))
    # Octet 27
    data.extend(uint1(self.perturbation_number))
    # Octet 28
    data.extend(uint1(self.number_of_forecasts))

def encode_derived_forecast_fields(self, data: bytearray):
    # Octet 26
    data.extend(uint1(self.derived_forecast_type))
    # Octet 27
    data.extend(uint1(self.number_of_forecasts))

def encode_statistical_processing_fields(self, data: bytearray):
    # Octets 26-27
    data.extend(uint2(self.end_year))
    # Octet 28
    data.extend(uint1(self.end_month))
    # Octet 29
    data.extend(uint1(self.end_day))
    # Octet 30
    data.extend(uint1(self.end_hour))
    # Octet 31
    data.extend(uint1(self.end_minute))
    # Octet 32
    data.extend(uint1(self.end_second))
    # Octet 33
    data.extend(uint1(self.number_of_time_ranges))
    # Octets 34-37
    data.extend(uint4(self.number_missing))
    # Octet 38
    data.extend(uint1(self.statistical_process))
    # Octet 39
    data.extend(uint1(self.time_increment_type))
    # Octet 40
    data.extend(uint1(self.statistical_time_unit))
    # Octets 41-44
    data.extend(uint4(self.statistical_time_length))
    # Octet 45
    data.extend(uint1(self.successive_time_unit))
    # Octets 46-49
    data.extend(uint4(self.successive_time_increment))

def encode_spatial_processing_fields(self, data: bytearray):
    # Octet 26
    data.extend(uint1(self.spatial_statistical_process))
    # Octet 27
    data.extend(uint1(self.spatial_processing_type))
    # Octets 28
    data.extend(uint1(self.number_of_points_used))

@dataclass(slots=True)
class ProductDefinitionTemplate0(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    @property
    def template_number(self) -> int:
        return 0
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionTemplate1(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    ensemble_type: EnsembleForecastType = EnsembleForecastType.UNPERTURBED_HIGH_RESOLUTION
    perturbation_number: int = 0
    number_of_forecasts: int = 1
    @property
    def template_number(self) -> int:
        return 1
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        encode_ensemble_fields(self, data)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionTemplate2(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    derived_forecast_type: DerivedForecastType = (DerivedForecastType.UNWEIGHTED_MEAN)
    number_of_forecasts: int = 1
    @property
    def template_number(self) -> int:
        return 2
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        encode_derived_forecast_fields(self, data)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionTemplate8(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    end_year: int = 2025
    end_month: int = 1
    end_day: int = 1
    end_hour: int = 6
    end_minute: int = 0
    end_second: int = 0
    number_of_time_ranges: int = 1
    number_missing: int = 0
    statistical_process: StatisticalProcess = StatisticalProcess.AVERAGE
    time_increment_type: int = 2
    statistical_time_unit: int = 1
    statistical_time_length: int = 6
    successive_time_unit: int = 1
    successive_time_increment: int = 0
    @property
    def template_number(self) -> int:
        return 8
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        encode_statistical_processing_fields(self, data)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionTemplate411(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    ensemble_type: EnsembleForecastType = EnsembleForecastType.UNPERTURBED_HIGH_RESOLUTION
    perturbation_number: int = 0
    number_of_forecasts: int = 1
    end_year: int = 2025
    end_month: int = 1
    end_day: int = 1
    end_hour: int = 6
    end_minute: int = 0
    end_second: int = 0
    number_of_time_ranges: int = 1
    number_missing: int = 0
    statistical_process: StatisticalProcess = StatisticalProcess.AVERAGE
    time_increment_type: int = 2
    statistical_time_unit: int = 1
    statistical_time_length: int = 6
    successive_time_unit: int = 1
    successive_time_increment: int = 0
    @property
    def template_number(self) -> int:
        return 11
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        encode_ensemble_fields(self, data)
        encode_statistical_processing_fields(self, data)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionTemplate12(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    derived_forecast_type: DerivedForecastType = (DerivedForecastType.UNWEIGHTED_MEAN)
    number_of_forecasts: int = 1
    end_year: int = 2025
    end_month: int = 1
    end_day: int = 1
    end_hour: int = 6
    end_minute: int = 0
    end_second: int = 0
    number_of_time_ranges: int = 1
    number_missing: int = 0
    statistical_process: StatisticalProcess = StatisticalProcess.AVERAGE
    time_increment_type: int = 2
    statistical_time_unit: int = 1
    statistical_time_length: int = 6
    successive_time_unit: int = 1
    successive_time_increment: int = 0
    @property
    def template_number(self) -> int:
        return 12
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        encode_derived_forecast_fields(self, data)
        encode_statistical_processing_fields(self, data)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionTemplate15(ProductDefinitionTemplate):
    parameter_category: int = 0
    parameter_number: int = 0
    generating_process_type: int = 0
    background_process_id: int = 0
    generating_process_id: int = 0
    hours_after_reference: int = 0
    minutes_after_reference: int = 0
    forecast_time_unit: int = 1
    forecast_time: int = 0
    surface_type: int = 100
    surface_scale_factor: int = 0
    surface_value: int = 500
    second_surface_type: int = 255
    second_surface_scale_factor: int = 0
    second_surface_value: int = 0
    spatial_statistical_process: SpatialStatisticalProcess = (SpatialStatisticalProcess.AVERAGE)
    spatial_processing_type: SpatialProcessingType = (SpatialProcessingType.RECTANGULAR)
    number_of_points_used: int = 9
    @property
    def template_number(self) -> int:
        return 15
    def encode(self) -> bytes:
        data = encode_template40_fields(self)
        encode_spatial_processing_fields(self, data)
        return bytes(data)