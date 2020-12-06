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

interface Response {
  difficulty: number;
  hash: string;
  nonce: number;
  prev_hash: string;
  timestamp: string;
  vote_info: {
    campaign_id: number;
    candidate_id: 1 | 2 | 3 | 4;
    timestamp: string;
    voter_id: string;
  };
}

export function BlockchainViewer() {
  const [blocks, setBlocks] = useState([]);

  const classes = useStyles();

  async function fetchData() {
    const response = await fetch("http://localhost:5000/api/getvotes");
    const data = await response.json();
    setBlocks(data);
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Container maxWidth="md">
      <Grid style={{ padding: "16px", margin: "16px" }}>
        {blocks.map(
          ({ hash, prev_hash, timestamp, vote_info }: Response, index) => (
            <Paper elevation={3} className={classes.paper}>
              <Typography variant="h5" component="h5">
                Block #{index + 1}
              </Typography>
              <Divider />
              <Typography>
                <strong className={classes.property}>VOTER ID:</strong>{" "}
                {vote_info.voter_id}
              </Typography>
              <Typography>
                <strong className={classes.property}>CAMPAIGN ID:</strong>{" "}
                {vote_info.campaign_id}
              </Typography>
              {vote_info.campaign_id != null ? (
                <>
                  <Typography>
                    <strong className={classes.property}>CAMPAIGN NAME:</strong>{" "}
                    {campaigns[vote_info.campaign_id - 1].title}
                  </Typography>
                  <Typography>
                    <strong className={classes.property}>CANDIDATE:</strong>{" "}
                    {
                      campaigns[vote_info.campaign_id - 1].candidates[
                        vote_info.candidate_id - 1
                      ]
                    }
                  </Typography>
                </>
              ) : null}
              <Divider />
              <Typography className={classes.text}>
                <strong className={classes.property}>HASH:</strong> {hash}
              </Typography>
              <Typography className={classes.text}>
                <strong className={classes.property}>PREVIOUS HASH:</strong>{" "}
                {prev_hash}
              </Typography>
              <Typography>
                <strong className={classes.property}>TIMESTAMP:</strong>{" "}
                {timestamp}
              </Typography>
            </Paper>
          )
        )}
      </Grid>
    </Container>
  );
}
