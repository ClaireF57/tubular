import datetime

import numpy as np
import pandas as pd
import pytest
import test_aide as ta

import tests.test_data as d
import tubular
from tubular.dates import DateDifferenceTransformer


class TestInit:
    """Tests for DateDifferenceTransformer.init()."""

    def test_arguments(self):
        """Test that init has expected arguments."""
        ta.functions.test_function_arguments(
            func=DateDifferenceTransformer.__init__,
            expected_arguments=[
                "self",
                "column_lower",
                "column_upper",
                "new_column_name",
                "units",
                "copy",
                "verbose",
            ],
            expected_default_values=(None, "D", True, False),
        )

    def test_class_methods(self):
        """Test that DateDifferenceTransformer has fit and transform methods."""
        x = DateDifferenceTransformer(
            "column_lower",
            "column_upper",
        )

        ta.classes.test_object_method(
            obj=x,
            expected_method="transform",
            msg="transform",
        )

    def test_inheritance(self):
        """Test that DateDifferenceTransformer inherits from BaseTransformer."""
        x = DateDifferenceTransformer("column_lower", "column_upper")

        ta.classes.assert_inheritance(x, tubular.base.BaseTransformer)

    def test_super_init_called(self, mocker):
        """Test that init calls BaseTransformer.init."""
        expected_call_args = {
            0: {
                "args": (),
                "kwargs": {
                    "columns": ["dummy_1", "dummy_2"],
                    "copy": True,
                    "verbose": False,
                },
            },
        }

        with ta.functions.assert_function_call(
            mocker,
            tubular.base.BaseTransformer,
            "__init__",
            expected_call_args,
        ):
            DateDifferenceTransformer(
                column_lower="dummy_1",
                column_upper="dummy_2",
                new_column_name="dummy_3",
                units="D",
            )

    def test_column_lower_type_error(self):
        """Test that an exception is raised if column_lower is not a str."""
        with pytest.raises(
            TypeError,
            match="DateDifferenceTransformer: column_lower must be a str",
        ):
            DateDifferenceTransformer(
                column_lower=123,
                column_upper="dummy_2",
                new_column_name="dummy_3",
                units="D",
                copy=True,
                verbose=False,
            )

    def test_column_2_type_error(self):
        """Test that an exception is raised if column_upper is not a str."""
        with pytest.raises(
            TypeError,
            match="DateDifferenceTransformer: column_upper must be a str",
        ):
            DateDifferenceTransformer(
                column_lower="dummy_1",
                column_upper=123,
                new_column_name="dummy_3",
                units="D",
                copy=True,
                verbose=False,
            )

    def test_new_column_name_type_error(self):
        """Test that an exception is raised if new_column_name is not a str."""
        with pytest.raises(
            TypeError,
            match="DateDifferenceTransformer: new_column_name must be a str",
        ):
            DateDifferenceTransformer(
                column_lower="dummy_1",
                column_upper="dummy_2",
                new_column_name=123,
                units="D",
                copy=True,
                verbose=False,
            )

    def test_units_type_error(self):
        """Test that an exception is raised if new_column_name is not a str."""
        with pytest.raises(
            TypeError,
            match="DateDifferenceTransformer: units must be a str",
        ):
            DateDifferenceTransformer(
                column_lower="dummy_1",
                column_upper="dummy_2",
                new_column_name="dummy_3",
                units=123,
                copy=True,
                verbose=False,
            )

    def test_units_values_error(self):
        """Test that an exception is raised if the value of inits is not one of accepted_values_units."""
        with pytest.raises(
            ValueError,
            match=r"DateDifferenceTransformer: units must be one of \['D', 'h', 'm', 's'\], got y",
        ):
            DateDifferenceTransformer(
                column_lower="dummy_1",
                column_upper="dummy_2",
                new_column_name="dummy_3",
                units="y",
                copy=True,
                verbose=False,
            )

    def test_inputs_set_to_attribute(self):
        """Test that the value passed for new_column_name and units are saved in attributes of the same name."""
        x = DateDifferenceTransformer(
            column_lower="dummy_1",
            column_upper="dummy_2",
            new_column_name="value_1",
            units="D",
            copy=True,
            verbose=False,
        )

        ta.classes.test_object_attributes(
            obj=x,
            expected_attributes={
                "columns": ["dummy_1", "dummy_2"],
                "new_column_name": "value_1",
                "units": "D",
                "copy": True,
                "verbose": False,
            },
            msg="Attributes for DateDifferenceTransformer set in init",
        )

    def test_inputs_set_to_attribute_name_not_set(self):
        """Test that the value passed for new_column_new_column_name and units are saved in attributes of the same new_column_name."""
        x = DateDifferenceTransformer(
            column_lower="dummy_1",
            column_upper="dummy_2",
            units="D",
            copy=True,
            verbose=False,
        )

        ta.classes.test_object_attributes(
            obj=x,
            expected_attributes={
                "column_lower": "dummy_1",
                "column_upper": "dummy_2",
                "columns": ["dummy_1", "dummy_2"],
                "new_column_name": "dummy_2_dummy_1_datediff_D",
                "units": "D",
                "copy": True,
                "verbose": False,
            },
            msg="Attributes for DateDifferenceTransformer set in init",
        )


class TestTransform:
    """Tests for DateDifferenceTransformer.transform()."""

    def expected_df_3():
        """Define expected output for test_expected_output_units_D."""
        return pd.DataFrame(
            {
                "a": [
                    datetime.datetime(1993, 9, 27, 11, 58, 58),
                    datetime.datetime(2000, 3, 19, 12, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 10, 59, 59),
                    datetime.datetime(2018, 12, 10, 11, 59, 59),
                    datetime.datetime(1985, 7, 23, 11, 59, 59),
                ],
                "b": [
                    datetime.datetime(2020, 5, 1, 12, 59, 59),
                    datetime.datetime(2019, 12, 25, 11, 58, 58),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 9, 10, 9, 59, 59),
                    datetime.datetime(2015, 11, 10, 11, 59, 59),
                    datetime.datetime(2015, 11, 10, 12, 59, 59),
                    datetime.datetime(2015, 7, 23, 11, 59, 59),
                ],
                "D": [
                    9713.042372685186,
                    7219.957627314815,
                    0.0,
                    31.0,
                    -30.083333333333332,
                    -1064.9583333333333,
                    -1125.9583333333333,
                    10957.0,
                ],
            },
        )

    def expected_df_4():
        """Define expected output for test_expected_output_units_h."""
        return pd.DataFrame(
            {
                "a": [
                    datetime.datetime(1993, 9, 27, 11, 58, 58),
                    datetime.datetime(2000, 3, 19, 12, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 10, 59, 59),
                    datetime.datetime(2018, 12, 10, 11, 59, 59),
                    datetime.datetime(1985, 7, 23, 11, 59, 59),
                ],
                "b": [
                    datetime.datetime(2020, 5, 1, 12, 59, 59),
                    datetime.datetime(2019, 12, 25, 11, 58, 58),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 9, 10, 9, 59, 59),
                    datetime.datetime(2015, 11, 10, 11, 59, 59),
                    datetime.datetime(2015, 11, 10, 12, 59, 59),
                    datetime.datetime(2015, 7, 23, 11, 59, 59),
                ],
                "h": [
                    233113.01694444445,
                    173278.98305555555,
                    0.0,
                    744.0,
                    -722.0,
                    -25559.0,
                    -27023.0,
                    262968.0,
                ],
            },
        )

    def expected_df_5():
        """Define expected output for test_expected_output_units_m."""
        return pd.DataFrame(
            {
                "a": [
                    datetime.datetime(1993, 9, 27, 11, 58, 58),
                    datetime.datetime(2000, 3, 19, 12, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 10, 59, 59),
                    datetime.datetime(2018, 12, 10, 11, 59, 59),
                    datetime.datetime(1985, 7, 23, 11, 59, 59),
                ],
                "b": [
                    datetime.datetime(2020, 5, 1, 12, 59, 59),
                    datetime.datetime(2019, 12, 25, 11, 58, 58),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 9, 10, 9, 59, 59),
                    datetime.datetime(2015, 11, 10, 11, 59, 59),
                    datetime.datetime(2015, 11, 10, 12, 59, 59),
                    datetime.datetime(2015, 7, 23, 11, 59, 59),
                ],
                "m": [
                    13986781.016666668,
                    10396738.983333332,
                    0.0,
                    44640.0,
                    -43320.0,
                    -1533540.0,
                    -1621380.0,
                    15778080.0,
                ],
            },
        )

    def expected_df_6():
        """Define expected output for test_expected_output_units_s."""
        return pd.DataFrame(
            {
                "a": [
                    datetime.datetime(1993, 9, 27, 11, 58, 58),
                    datetime.datetime(2000, 3, 19, 12, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 11, 59, 59),
                    datetime.datetime(2018, 10, 10, 10, 59, 59),
                    datetime.datetime(2018, 12, 10, 11, 59, 59),
                    datetime.datetime(1985, 7, 23, 11, 59, 59),
                ],
                "b": [
                    datetime.datetime(2020, 5, 1, 12, 59, 59),
                    datetime.datetime(2019, 12, 25, 11, 58, 58),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 11, 10, 11, 59, 59),
                    datetime.datetime(2018, 9, 10, 9, 59, 59),
                    datetime.datetime(2015, 11, 10, 11, 59, 59),
                    datetime.datetime(2015, 11, 10, 12, 59, 59),
                    datetime.datetime(2015, 7, 23, 11, 59, 59),
                ],
                "s": [
                    839206861.0,
                    623804339.0,
                    0.0,
                    2678400.0,
                    -2599200.0,
                    -92012400.0,
                    -97282800.0,
                    946684800.0,
                ],
            },
        )

    def expected_df_7():
        """Define expected output for test_expected_output_nulls."""
        return pd.DataFrame(
            {
                "a": [
                    datetime.datetime(1993, 9, 27, 11, 58, 58),
                    np.NaN,
                ],
                "b": [
                    np.NaN,
                    datetime.datetime(2019, 12, 25, 11, 58, 58),
                ],
                "D": [
                    np.NaN,
                    np.NaN,
                ],
            },
            index=[0, 1],
        )

    def test_arguments(self):
        """Test that transform has expected arguments."""
        ta.functions.test_function_arguments(
            func=DateDifferenceTransformer.transform,
            expected_arguments=["self", "X"],
        )

    def test_super_transform_called(self, mocker):
        """Test that BaseTransformer.transform called."""
        df = d.create_datediff_test_df()

        x = DateDifferenceTransformer(
            column_lower="a",
            column_upper="b",
            new_column_name="D",
            units="D",
            copy=True,
            verbose=False,
        )

        expected_call_args = {0: {"args": (d.create_datediff_test_df(),), "kwargs": {}}}

        with ta.functions.assert_function_call(
            mocker,
            tubular.base.BaseTransformer,
            "transform",
            expected_call_args,
            return_value=d.create_datediff_test_df(),
        ):
            x.transform(df)

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(
            d.create_datediff_test_df(),
            expected_df_3(),
        ),
    )
    def test_expected_output_units_D(self, df, expected):
        """Test that the output is expected from transform, when units is D.

        This tests positive month gaps, negative month gaps, and missing values.

        """
        x = DateDifferenceTransformer(
            column_lower="a",
            column_upper="b",
            new_column_name="D",
            units="D",
            copy=True,
            verbose=False,
        )

        df_transformed = x.transform(df)

        ta.equality.assert_equal_dispatch(
            expected=expected,
            actual=df_transformed,
            msg="Unexpected values in DateDifferenceYearTransformer.transform",
        )

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(
            d.create_datediff_test_df(),
            expected_df_4(),
        ),
    )
    def test_expected_output_units_h(self, df, expected):
        """Test that the output is expected from transform, when units is h.

        This tests positive month gaps, negative month gaps, and missing values.

        """
        x = DateDifferenceTransformer(
            column_lower="a",
            column_upper="b",
            new_column_name="h",
            units="h",
            copy=True,
            verbose=False,
        )

        df_transformed = x.transform(df)

        ta.equality.assert_equal_dispatch(
            expected=expected,
            actual=df_transformed,
            msg="Unexpected values in DateDifferenceYearTransformer.transform",
        )

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(
            d.create_datediff_test_df(),
            expected_df_5(),
        ),
    )
    def test_expected_output_units_m(self, df, expected):
        """Test that the output is expected from transform, when units is m.

        This tests positive month gaps, negative month gaps, and missing values.

        """
        x = DateDifferenceTransformer(
            column_lower="a",
            column_upper="b",
            new_column_name="m",
            units="m",
            copy=True,
            verbose=False,
        )

        df_transformed = x.transform(df)

        ta.equality.assert_equal_dispatch(
            expected=expected,
            actual=df_transformed,
            msg="Unexpected values in DateDifferenceYearTransformer.transform",
        )

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(
            d.create_datediff_test_df(),
            expected_df_6(),
        ),
    )
    def test_expected_output_units_s(self, df, expected):
        """Test that the output is expected from transform, when units is s.

        This tests positive month gaps, negative month gaps, and missing values.

        """
        x = DateDifferenceTransformer(
            column_lower="a",
            column_upper="b",
            new_column_name="s",
            units="s",
            copy=True,
            verbose=False,
        )

        df_transformed = x.transform(df)

        ta.equality.assert_equal_dispatch(
            expected=expected,
            actual=df_transformed,
            msg="Unexpected values in DateDifferenceYearTransformer.transform",
        )

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(
            d.create_datediff_test_nulls_df(),
            expected_df_7(),
        ),
    )
    def test_expected_output_nulls(self, df, expected):
        """Test that the output is expected from transform, when columns are nulls."""
        x = DateDifferenceTransformer(
            column_lower="a",
            column_upper="b",
            new_column_name="D",
            units="D",
            copy=True,
            verbose=False,
        )

        df_transformed = x.transform(df)

        ta.equality.assert_frame_equal_msg(
            actual=df_transformed,
            expected=expected,
            msg_tag="Unexpected values in DateDifferenceTransformer.transform (nulls)",
        )
