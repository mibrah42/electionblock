import { Container, Divider, Grid, makeStyles, Paper, Typography } from '@material-ui/core';
import React, { useEffect, useState } from 'react';

export const candidatesMap = {
    1: 'Donald Trump',
    2: 'Joe Biden',
    3: 'Kanye West',
    4: 'I\'ll pass on this one'
}

export const campaignMap = {
    1: 'US Elections'
}

const useStyles = makeStyles({
    paper: {
        padding: "16px",
        marginBottom: "16px",
        textAlign: 'left',
        flexWrap: 'wrap',
        flexShrink: 1
    },
    text: {
        flexShrink: 1
    }
  });

interface Response {
    difficulty: number;
    hash: string;
    nonce: number;
    prev_hash: string;
    timestamp: string;
    vote_info: {
        campaign_id: number,
        candidate_id: 1 | 2 | 3 | 4,
        timestamp: string,
        voter_id: string,
    },
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
        <Grid style={{padding: '16px', margin: '16px'}}>
        {
            blocks.map(({hash, prev_hash, nonce, difficulty, timestamp, vote_info}: Response, index) => 
                <Paper elevation={3} className={classes.paper}>
                    <Typography>Block #{index + 1}</Typography>
                    <Divider />
                    <Typography>Voter ID: {vote_info.voter_id}</Typography>
                    <Typography>Campaign ID: {vote_info.campaign_id}</Typography>
                    <Typography>Candidate: {candidatesMap[vote_info.candidate_id]}</Typography>
                    <Divider />
                    <Typography className={classes.text}>Hash: {hash}</Typography>
                    <Typography className={classes.text}>Previous Hash: {prev_hash}</Typography>
                    <Typography>Timestamp: {timestamp}</Typography>
                    <Typography>Nonce: {nonce}</Typography>
                    <Typography>Difficulty: {difficulty}</Typography>
                </Paper>
            )
        }
        </Grid>
        </Container>
    )
}