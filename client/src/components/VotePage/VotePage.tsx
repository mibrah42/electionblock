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

const ENDPOINT = "http://127.0.0.1:6001";

export function VotePage({
  match,
}: RouteComponentProps<{ campaign_id: string }>) {
  const [candidate, setCandidate] = useState("");
  // const [voter, setVoter] = useState<string | null>(null);
  const classes = useStyles();
  const campaign = useMemo(() => match.params.campaign_id, []);
  // const [title, setTitle] = useState("Scan fingerprint to vote");
  // const [disabled, setDisabled] = useState(false);

  // useEffect(() => {
  //   const socket = socketIOClient(ENDPOINT);
  //   socket.on("fingerprint", (response: Response) => {
  //     handleResponse(response);
  //   });
  // }, []);

  // function handleResponse({ type, message, payload }: Response) {
  //   if (type === "FINGERPRINT_FOUND") {
  //     setVoter(payload);
  //     setDisabled(true);
  //   }

  //   setTitle(message);
  // }

  const handleChange = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setCandidate(event.target.value);
  };

  async function addBlock() {
    const VOTE_URL = `http://localhost:5000/api/vote`;

    const response = await fetch(VOTE_URL, {
      method: "post",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
        "Accept-Charset": "utf-8",
      },
      body: JSON.stringify({
        data: {
          voter_id: "1",
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
          Scan finger to vote
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
                  onClick={addBlock}
                  style={{ width: "100%", backgroundColor: "#B82B3F" }}
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
