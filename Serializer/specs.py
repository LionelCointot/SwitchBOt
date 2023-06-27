# pylint: disable=empty-docstring, missing-class-docstring,
# pylint: disable=missing-function-docstring, missing-module-docstring
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from types import ModuleType
from typing import Optional

import cdl

from serializer import (
    DataclassSerializer,
    EnumSerializer,
    ValueSerializerBase,
    dumper,
    loader,
)

# ============================================================================
#
#       Helpers class
#
# ============================================================================


# @xxx.register
class Module:
    """ """

    def __init__(self, module: ModuleType):
        self.module = module

    def __copy__(self):
        return self.module.__name__

    def __deepcopy__(self, memo):
        return self.module.__name__

    def __str__(self) -> str:
        return f"{type(self).__qualname__}(module={self.module})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Module):
            return self.module == __value.module
        return False

    def __serialize__(self) -> str:
        return self.module.__name__

    @classmethod
    def __deserialize__(cls, obj: str) -> "Module":
        try:
            return cls(sys.modules[obj])
        except KeyError:
            print("ici")
            __import__(obj)
            return cls(sys.modules[obj])


class ModuleSerializer(ValueSerializerBase[Module, str]):
    def serialize(self, obj: Module) -> str:
        return obj.__serialize__()

    def deserialize(self, obj: str) -> Module:
        return Module.__deserialize__(obj)


# ============================================================================
#
#       Enums
#
# ============================================================================


@EnumSerializer.register
class ResultEnum(Enum):
    """Results value for a test."""

    NOT_EXECUTED = "not_executed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ACCEPTED_WITH_RESERVES = "accepted_with_reserves"


# ============================================================================
#
#       Registered classes
#
# ============================================================================


@DataclassSerializer.register
@dataclass
class TestResult:
    """ """

    result: ResultEnum
    execution_duration: timedelta
    last_run: datetime
    comment: Optional[str] = None
    error_code: Optional[str] = None
    error_msg: Optional[str] = None


@DataclassSerializer.register
@dataclass
class Test:
    """ """

    path: str
    test_module: Module
    description: str = ""
    result: Optional[TestResult] = None
    command_line: str = ""

    def run_test(self):
        """Runs test"""

    def export_test(self):
        """ """

    def export_param(self):
        """Export TestParam"""

    def export_result(self):
        """Export results"""


@DataclassSerializer.register
@dataclass
class TestSuite:
    """ """

    package: Module
    testmgr_path: Optional[str] = None
    description: str = ""
    tests: list[Test] = field(default_factory=list)
    up_to_date: bool = False  # ? Enum
    last_run: Optional[datetime] = None
    author: str = ""

    def reload(self, testmgr_path):
        """ """

    def save_as(self, testmgr_path):
        """ """

    def save(self):
        """ """

    def open(self, testmgr_path: str):
        """ """

    def export_suite(self):
        """ """

    def run_tests(self, test_list: list[Test], is_batch_mode: bool = False):
        """ """

    def kill_tests(self):
        """ """


# ============================================================================
#
#       Serializers
#
# ============================================================================


def serial_poc(file_path):
    """ """
    test_result = TestResult(ResultEnum.ACCEPTED, timedelta(0, 3, 298), datetime.now())
    a_result = TestResult(ResultEnum.REJECTED, timedelta(8, 43, 15932), datetime.now())

    test = Test("C:\\", Module(sys), result=test_result)
    another_test = Test("C:\\", Module(json), result=a_result)

    test_suite = TestSuite(Module(cdl))
    test_suite.tests.append(test)
    test_suite.tests.append(another_test)

    dumper(file_path, test_suite)
    return test_suite


def deserial_poc(file_path):
    """ """
    test_suite = loader(file_path)
    return test_suite


if __name__ == "__main__":
    POC_PATH = r"C:\_projets\test_manager\sample\test_poc.testmgr"
    EQ_PATH = r"C:\_projets\test_manager\sample\test_eq.testmgr"
    serial_suite = serial_poc(POC_PATH)
    deserial_suite = deserial_poc(POC_PATH)
    dumper(EQ_PATH, deserial_suite)

    print(serial_suite == deserial_suite)
