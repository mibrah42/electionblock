import {
  Button,
  CircularProgress,
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
  vote: {
    paddingTop: 16,
    paddingBottom: 16,
  },
  loadingContainer: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: 600,
  },
});

interface Vote {
  campaign_id: number;
  candidate_id: 1 | 2 | 3 | 4;
  timestamp: string;
  voter_id: string;
}

interface Response {
  difficulty: number;
  hash: string;
  nonce: number;
  prev_hash: string;
  timestamp: string;
  votes: Vote[];
}

export function BlockchainViewer() {
  const [blocks, setBlocks] = useState([]);
  const [loadingShardCount, setLoadingShardCount] = useState(false);
  const [loadingBlocks, setLoadingBlocks] = useState(false);
  const [shardCount, setShardCount] = useState(0);
  const [selectedShard, setSelectedShard] = useState(0);
  const classes = useStyles();

  async function fetchData(shard: number) {
    try {
      setLoadingBlocks(true);
      const response = await fetch(
        `http://localhost:5000/api/getvotes/${shard}`
      );
      const data = await response.json();
      setBlocks(data.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingBlocks(false);
    }
  }

  async function fetchShardCount() {
    try {
      setLoadingShardCount(true);
      const response = await fetch(
        "http://localhost:5000/api/get_shards_length"
      );
      const data = await response.json();
      setShardCount(data.length);
      return data.length;
    } catch (e) {
      console.error(e);
      return null;
    } finally {
      setLoadingShardCount(false);
    }
  }

  async function initialLoad() {
    const shardCount = await fetchShardCount();
    if (shardCount != null && shardCount > 0) {
      fetchData(0);
    }
  }

  useEffect(() => {
    initialLoad();
  }, []);

  if (loadingShardCount) {
    return (
      <Container maxWidth="md" className={classes.loadingContainer}>
        <CircularProgress />
      </Container>
    );
  }

  if (shardCount == null || shardCount == 0) {
    return (
      <Container maxWidth="md" className={classes.loadingContainer}>
        <Typography variant="h5" component="h5">
          Blockchain is empty
        </Typography>
      </Container>
    );
  }

  const shardSelection = [];
  for (let i = 0; i < shardCount; i++) {
    shardSelection.push(
      <Button
        disabled={i === selectedShard}
        variant="contained"
        onClick={() => {
          fetchData(i);
          setSelectedShard(i);
        }}
        style={{ margin: 4 }}
      >
        Shard {i}
      </Button>
    );
  }

  return (
    <Container maxWidth="md">
      <Grid style={{ padding: "16px", marginLeft: 8, marginRight: 8 }}>
        {shardSelection}
      </Grid>
      {loadingBlocks ? (
        <Container maxWidth="md" className={classes.loadingContainer}>
          <CircularProgress />
        </Container>
      ) : (
        <Grid style={{ padding: "16px", marginLeft: 12, marginRight: 12 }}>
          {blocks.map(
            ({ hash, prev_hash, timestamp, votes }: Response, index) => {
              return (
                <Paper key={hash} elevation={3} className={classes.paper}>
                  <Typography variant="h5" component="h5">
                    Block #{index + 1}
                  </Typography>
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
                  <Divider />
                  {votes.map(
                    ({ campaign_id, candidate_id, timestamp, voter_id }) => (
                      <div
                        key={`${voter_id}${campaign_id}`}
                        className={classes.vote}
                      >
                        <Typography>
                          <strong className={classes.property}>
                            VOTER ID:
                          </strong>{" "}
                          {voter_id}
                        </Typography>
                        <Typography>
                          <strong className={classes.property}>
                            CAMPAIGN ID:
                          </strong>{" "}
                          {campaign_id}
                        </Typography>
                        {campaign_id != null ? (
                          <>
                            <Typography>
                              <strong className={classes.property}>
                                CAMPAIGN NAME:
                              </strong>{" "}
                              {campaigns[campaign_id - 1].title}
                            </Typography>
                            <Typography>
                              <strong className={classes.property}>
                                CANDIDATE:
                              </strong>{" "}
                              {
                                campaigns[campaign_id - 1].candidates[
                                  candidate_id - 1
                                ]
                              }
                            </Typography>
                            <Typography>
                              <strong className={classes.property}>
                                TIMESTAMP:
                              </strong>{" "}
                              {timestamp}
                            </Typography>
                          </>
                        ) : null}
                      </div>
                    )
                  )}
                </Paper>
              );
            }
          )}
        </Grid>
      )}
    </Container>
  );
}
