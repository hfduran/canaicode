import { Box, Button, Modal, SpaceBetween } from "@cloudscape-design/components";
import Filters from "./Filters";
import { useDataFiltering } from "../hooks";
import { DashboardData, FlattenedDataEntry } from "../types/ui";
import { useEffect } from "react";

interface props {
    data: DashboardData[],
    setFilteredData: (x: FlattenedDataEntry[]) => void;
    visible: boolean;
    setVisible: (x: boolean) => void;
}

export const DashboardFiltersModal: React.FC<props> = ({data, setFilteredData, visible, setVisible}) => {
  const {
    filteredData,
    availableLanguages,
    availableTeams,
    tempFilters,
    setTempFilters,
    handleApplyFilters,
    handleCancelFilters,
    handleResetFilters,
  } = useDataFiltering(data, () => {setVisible(false)});

  useEffect(() => {
    setFilteredData(filteredData)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filteredData])

  return (
    <Modal
      onDismiss={handleCancelFilters}
      visible={visible}
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button variant="normal" onClick={handleResetFilters}>
              Reset Filters
            </Button>
            <Button variant="link" onClick={handleCancelFilters}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleApplyFilters}>
              Apply Filters
            </Button>
          </SpaceBetween>
        </Box>
      }
      header="Chart Filters"
    >
      <Filters
        filters={tempFilters}
        setFilters={setTempFilters}
        availableLanguages={Array.from(availableLanguages)}
        availableTeams={Array.from(availableTeams)}
      />
    </Modal>
  );
};
