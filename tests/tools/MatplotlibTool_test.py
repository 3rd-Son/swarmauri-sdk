import os
import pytest
from swarmauri.standard.tools.concrete.MatplotlibTool import MatplotlibTool as Tool

@pytest.mark.unit
def test_ubc_resource():
    tool = Tool()
    assert tool.resource == 'Tool'

@pytest.mark.unit
def test_ubc_type():
    assert Tool().type == 'MatplotlibTool'

@pytest.mark.unit
def test_initialization():
    tool = Tool()
    assert type(tool.id) == str

@pytest.mark.parametrize(
    "plot_type, x_data, y_data, title, x_label, y_label, save_path",
    [
        ("line", [1, 2, 3], [4, 5, 6], "Line Plot", "X-axis", "Y-axis", "test_line_plot.png"),
        ("bar", [1, 2, 3], [4, 5, 6], "Bar Plot", "X-axis", "Y-axis", "test_bar_plot.png"),
        ("scatter", [1, 2, 3], [4, 5, 6], "Scatter Plot", "X-axis", "Y-axis", "test_scatter_plot.png"),
    ]
)

@pytest.mark.unit
def test_call(plot_type, x_data, y_data, title, x_label, y_label, save_path):
    tool = Tool()
    result = tool(plot_type, x_data, y_data, title, x_label, y_label, save_path)

    assert result == save_path

    assert os.path.exists(save_path)

    os.remove(save_path)