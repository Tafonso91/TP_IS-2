"use client"
import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import FlagIcon from '@mui/icons-material/Flag';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import ContactsIcon from '@mui/icons-material/Contacts';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "country", label: "Country", Icon: FlagIcon},
    {"key": "number", label: "Shirt Number", Icon: ContactsIcon},
    {"key": "position", label: "Position", Icon: PictureInPictureAltIcon}
];

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties;
    const {id, imgUrl, name, country, number, position} = properties;
    const coordinates = geoJSON?.geometry?.coordinates;

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: imgUrl,
                iconRetinaUrl: imgUrl,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgUrl}/>
                        </ListItemIcon>
                        <ListItemText primary={name}/>
                    </ListItem>
                    {/* Adição de informações sobre o jogador */}
                    <ListItem>
                        <ListItemIcon>
                            <FlagIcon style={{color: "black"}}/>
                        </ListItemIcon>
                        <ListItemText
                            primary={<span>
                                {country} - {coordinates[0]}, {coordinates[1]}<br/>
                                <label style={{fontSize: "xx-small"}}>(Country - Coordinates)</label>
                            </span>}
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <ContactsIcon style={{color: "black"}}/>
                        </ListItemIcon>
                        <ListItemText
                            primary={<span>
                                Shirt Number: {number}<br/>
                                <label style={{fontSize: "xx-small"}}>(Shirt Number)</label>
                            </span>}
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <PictureInPictureAltIcon style={{color: "black"}}/>
                        </ListItemIcon>
                        <ListItemText
                            primary={<span>
                                Position: {position}<br/>
                                <label style={{fontSize: "xx-small"}}>(Position)</label>
                            </span>}
                        />
                    </ListItem>
                </List>
            </Popup>
        </Marker>
    )
}