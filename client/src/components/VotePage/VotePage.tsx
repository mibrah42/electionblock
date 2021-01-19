import React, { useEffect, useMemo, useState } from "react";
import Paper from "@material-ui/core/Paper";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import { makeStyles } from "@material-ui/core/styles";
import { Button, Container, Grid, Typography } from "@material-ui/core";
import fingerprintGif from "../../assets/fingerprint.gif";
import { RouteComponentProps } from "react-router-dom";
import { campaigns } from "../../data/campaigns";
import socketIOClient from "socket.io-client";

const useStyles = makeStyles({
  voteCard: {
    display: "flex",
  },
  wrapper: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "100%",
    marginTop: "30px",
  },
  radioGroup: {
    marginTop: "8px",
    marginBottom: "16px",
  },
  paper: {
    padding: "16px",
    display: "flex",
    flexDirection: "column",
  },
  radio: {
    "&$checked": {
      color: "#B82B3F",
    },
  },
  checked: {},
});

interface Response {
  type: string;
  message: string;
  payload: string;
}

const ENDPOINT = "http://192.168.2.79:6001/";
const VOTE_URL = "http://localhost:6002/api/vote";

export function VotePage({
  match,
}: RouteComponentProps<{ campaign_id: string }>) {
  const [candidate, setCandidate] = useState("");
  const classes = useStyles();
  const [voterId, setVoterId] = useState("1");
  const [disabled, setDisabled] = useState(false);
  const [title, setTitle] = useState("Scan finger to vote");
  const campaign = useMemo(() => match.params.campaign_id, []);

  async function fingerprintScan({ type, payload }: any) {
    if (type === "FINGERPRINT_FOUND") {
      // Check if voter id exists.
      try {
        const response = await fetch(
          `http://localhost:5000/api/hasvoted/${campaign}/${payload}`
        );
        const data = await response.json();
        console.log({ data });
        if (!data.has_voted) {
          setVoterId(payload);
          setDisabled(false);
          setTitle("Vote for candidate");
        } else {
          setTitle("Voter already voted");
        }
      } catch (e) {
        console.error(e);
      }
    }
  }

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on("fingerprint", fingerprintScan);
    return () => {
      socket.off("fingerprint", fingerprintScan);
    };
  }, []);

  const handleChange = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setCandidate(event.target.value);
  };

  async function addBlock() {
    const response = await fetch(VOTE_URL, {
      method: "post",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
        "Accept-Charset": "utf-8",
      },
      body: JSON.stringify({
        data: {
          voter_id: voterId,
          campaign_id: parseInt(campaign),
          candidate_id: parseInt(candidate),
          timestamp: Date.now(),
        },
      }),
    });

    const messageData = await response.json();

    console.log({ messageData });

    // the API frequently returns 201
    if (response.status !== 200 && response.status !== 201) {
      console.error(`Invalid response status ${response.status}.`);
      throw messageData;
    }
  }

  return (
    <Container className={classes.wrapper} maxWidth="sm">
      <Paper elevation={3} className={classes.paper}>
        <Typography
          variant="subtitle1"
          component="h2"
          style={{ fontWeight: "bold", margin: "0 auto" }}
        >
          {title}
        </Typography>
        <Grid>
          <Grid className={classes.voteCard}>
            <img src={fingerprintGif} alt="loading..." height={100} />
            <Grid>
              <FormControl component="fieldset">
                <RadioGroup
                  aria-label="voteForm"
                  name="voteForm"
                  value={candidate}
                  onChange={handleChange}
                  className={classes.radioGroup}
                >
                  {campaigns[parseInt(campaign) - 1].candidates.map(
                    (name, index) => (
                      <FormControlLabel
                        key={name + index}
                        control={
                          <Radio
                            disableRipple
                            classes={{
                              root: classes.radio,
                              checked: classes.checked,
                            }}
                          />
                        }
                        value={(index + 1).toString()}
                        label={name}
                      />
                    )
                  )}
                </RadioGroup>
                <Button
                  variant="contained"
                  color="primary"
                  disabled={disabled}
                  onClick={addBlock}
                  style={{
                    width: "100%",
                    backgroundColor: disabled ? "#8395A7" : "#B82B3F",
                  }}
                >
                  Vote
                </Button>
              </FormControl>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
}
