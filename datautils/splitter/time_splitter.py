"""
Module: time_splitter

This module provides functions to split summary data into training and validation sets based on time-domain.
"""

import model.summarymodel as sm
import datautils.splitter.summary_splitter as splitter
import numpy as np

def time_data_splitter(summaries: list[sm.SummaryModel]):
    """Split summaries into training and validation sets based on time-domain data."""
    X_train, X_val, y_train, y_val = splitter.summaries_data_splitter(summaries)

    X_train_time_data = np.array([summary.signal.get_time_data() for summary in X_train])
    X_val_time_data = np.array([summary.signal.get_time_data() for summary in X_val])

    return X_train_time_data, X_val_time_data, y_train, y_val

def segmented_time_data_splitter(summaries: list[sm.SummaryModel]):
    """Split segmented summaries into training and validation sets based on time-domain data."""
    X_train, X_val, y_train, y_val = splitter.segmented_summaries_data_splitter(summaries)

    X_train_segmented_time_data = np.concatenate([summary.signal.get_time_segmented_data() for summary in X_train])
    X_val_segmented_time_data = np.concatenate([summary.signal.get_time_segmented_data() for summary in X_val])

    return X_train_segmented_time_data, X_val_segmented_time_data, y_train, y_val