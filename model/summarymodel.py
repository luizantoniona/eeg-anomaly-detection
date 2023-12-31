import reader.mnereader as mnereader
import reader.reader as reader
import model.mnesignalmodel as mnesignal
class SummaryModel:

    """
    A class representing a summary of data.

    Attributes:
    - record_name (str): Name of the record.
    - file_name (str): Name of the data file.
    - start_time (str): Start time of the data.
    - end_time (str): End time of the data.
    - nr_seizures (int): Number of seizures in the data.
    - start_seizure (list): List of start times of seizures.
    - end_seizure (list): List of end times of seizures.
    - nr_channels (int): Number of data channels.
    - ds_channels (list): List of data channels.
    - signal: An instance of signal model (MNESignalModel).
    """

    def __init__(self, record_name, file_name, start_time, end_time, nr_seizures, start_seizure, end_seizure, nr_channels, ds_channels):
        self.record_name = record_name
        self.file_name = file_name
        self.start_time = start_time
        self.end_time = end_time
        self.nr_seizures = nr_seizures
        self.start_seizure = start_seizure
        self.end_seizure = end_seizure
        self.nr_channels = nr_channels
        self.ds_channels = ds_channels
        self.signal = None

    def __str__(self):
        return f"{self.record_name}:({self.file_name})"
    
    def fullpath(self):
        """
        Return the full path of the data file.
        """
        return "./data/" + self.record_name + "/" + self.file_name
    
    def duration(self):
        """
        Return the duration of the data in seconds.
        """
        duration = self.end_time - self.start_time
        return duration.total_seconds()
    
    def start_time_of_seizure(self, nr_seizure = 0):
        """
        Return the start time of a specific seizure.
        """
        if nr_seizure > self.nr_seizures:
            return 0
        else:
            return self.start_seizure[nr_seizure - 1]
        
    def end_time_of_seizure(self, nr_seizure = 0):
        """
        Return the end time of a specific seizure.
        """
        if nr_seizure > self.nr_seizures:
            return 0
        else:
            return self.end_seizure[nr_seizure - 1]
        
    def has_anomaly(self) -> bool:
        """
        Check if there are anomaly.
        """
        return self.nr_seizures > 0
    
    def has_anomaly_in_interval(self, tmin, tmax) -> bool:
        """
        Check if there are anomaly in time interval.
        """
        has_anomaly = False

        for i in range(self.nr_seizures):
            if self.start_time_of_seizure(i) <= tmin < self.end_time_of_seizure(i) or self.start_time_of_seizure(i) < tmax <= self.end_time_of_seizure(i):
                has_anomaly = True
            
        return has_anomaly
    
    def anomalies_by_time_window(self, time_window=5):
        """
        Check for anomalies in the data at regular intervals of a specified time window.
        """
        anomalies = []
        current_time = 0
        while current_time + time_window <= self.duration():
            anomalies.append(self.has_anomaly_in_interval(current_time, current_time + time_window))
            current_time += time_window

        return anomalies

    def generate_mne(self, rename = False) -> None:
        """
        Generate an MNE signal model.
        """
        self.signal =  mnesignal.MNESignalModel( mnereader.mne_edf(self, rename) )

    def generate_segmented_time_data(self, time_window=5):
        """
        Generate segmented time data based on a specified time window.
        """
        current_time = 0
        while current_time + time_window <= self.duration():
            self.signal.segment_time_data_by_interval(current_time, current_time + time_window)
            current_time += time_window

    def generate_segmented_freq_data(self, time_window=5):
        """
        Generate segmented frequency data based on a specified time window.
        """
        current_time = 0
        while current_time + time_window <= self.duration():
            self.signal.segment_freq_data_by_interval(current_time, current_time + time_window)
            current_time += time_window

    def generate_segmented_time_freq_data(self, time_window=5):
        """
        Generate segmented time-frequency data based on a specified time window.
        """
        current_time = 0
        while current_time + time_window <= self.duration():
            self.signal.segment_time_freq_data_by_interval(current_time, current_time + time_window)
            current_time += time_window