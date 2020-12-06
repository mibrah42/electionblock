import {
  Container,
  Divider,
  Grid,
  makeStyles,
  Paper,
  Typography,
} from "@material-ui/core";
import React, { useEffect, useState } from "react";
import { campaigns } from "../../data/campaigns";

const useStyles = makeStyles({
  paper: {
    padding: "16px",
    marginBottom: "16px",
    textAlign: "left",
    flexWrap: "wrap",
    flexShrink: 1,
  },
  text: {
    flexShrink: 1,
  },
  property: {
    color: "#2d3436",
  },
});

interface Props {}

export function Stats(props: Props) {
  const [data, setData] = useState<{ [campaignId: string]: string }>({});

  const classes = useStyles();

  async function fetchData() {
    const response = await fetch("http://localhost:5000/api/getstats");
    const statsData = await response.json();
    setData(statsData);
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Container maxWidth="md">
      <Grid style={{ padding: "16px", margin: "16px" }}>
        {Object.keys(data).map((campaign) => {
          const campaignId = parseInt(campaign) - 1;
          return (
            <Paper elevation={3} className={classes.paper}>
              <Typography variant="h5" component="h5">
                Campaign: {campaigns[campaignId].title}
              </Typography>
              <Divider />
              {campaigns[campaignId].candidates.map((candidate, index) => {
                return (
                  <Typography>
                    <strong className={classes.property}>{candidate}:</strong>{" "}
                    {data.hasOwnProperty((campaignId + 1).toString()) &&
                    data[(campaignId + 1).toString()].hasOwnProperty(index + 1)
                      ? data[(campaignId + 1).toString()][index + 1]
                      : 0}
                  </Typography>
                );
              })}
            </Paper>
          );
        })}
      </Grid>
    </Container>
  );
}
