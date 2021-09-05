import React from 'react';
import cx from 'clsx';
import {makeStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import ChevronRightRounded from '@material-ui/icons/ChevronRightRounded';
import TextInfoContent from '@mui-treasury/components/content/textInfo';
import {useWideCardMediaStyles} from '@mui-treasury/styles/cardMedia/wide';
import {useN01TextInfoContentStyles} from '@mui-treasury/styles/textInfoContent/n01';
import {useBouncyShadowStyles} from '@mui-treasury/styles/shadow/bouncy';

const useStyles = makeStyles(() => ({
    root: {
        maxWidth: 304,
        minWidth: 304,
        margin: 'auto',
        boxShadow: 'none',
        borderRadius: 16,
        border: 1
    },
    content: {
        padding: 24,
    },
    cta: {
        marginTop: 60,
        textTransform: 'initial',
    },
}));

export default function NewsCard(props) {

    const styles = useStyles();
    const mediaStyles = useWideCardMediaStyles();
    const textCardContentStyles = useN01TextInfoContentStyles();
    const shadowStyles = useBouncyShadowStyles();
    return (
        <div>

        <Card className={cx(styles.root, shadowStyles.root)}>
            <CardMedia
                classes={mediaStyles}

                image={props.image}
            />
            <CardContent className={styles.content}>
                <TextInfoContent
                    classes={textCardContentStyles}
                    overline={props.date}
                    heading={props.heading}
                    body={
                        props.body
                    }
                />
                <a target="_blank" href={props.url}>
                    <Button color={'primary'} fullWidth className={styles.cta}>
                        Find Out More <ChevronRightRounded/>
                    </Button>
                </a>
            </CardContent>
        </Card>
        </div>
    );
}

