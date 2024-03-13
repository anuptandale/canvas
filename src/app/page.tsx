"use client"
import React, { useEffect, useState } from 'react'
import TextField from '@mui/material/TextField';
import ImageIcon from '@mui/icons-material/Image';
import { ColorPicker, useColor } from "react-color-palette";
import "react-color-palette/css";

const page = () => {
  const [image, setImage] = useState(null);
  const [text, setText] = useState("")
  const [cta, setCta] = useState("")
  const [color, setColor] = useColor("#561ecb");
  const [selColor, setSelColor] = useState("red");
  const handleImageChange = (e: any) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  const handletext = (e: any) => {
    const newText = e.target.value.slice(0, 31); // Limiting to 31 characters
    setText(newText);
  }
  const handlecta = (e: any) => {
    setCta(e.target.value);
  }
  useEffect(()=>{
    console.log(color);
    setSelColor(color.hex);
  },[color])
  return (
    <div style={{ display: "flex", gap: "20px" }}>
      <div style={{ width: "1080px", height: "1080px",borderRadius:"5px",backgroundColor:"lightgrey", border: "1px solid grey", display: "flex", justifyContent: "center", alignItems: "center" }}>
        <div style={{ height: "400px", width: "500px", border: "3px solid black", background: `repeating-linear-gradient(to bottom, ${selColor},${selColor} 20px, white 20px, white 40px)` }}>
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginTop: "20px" }}>
            {image && (
              <img
                src={image}
                alt="Uploaded"
                style={{ maxWidth: "300px", borderRadius: "20px" }}
              />
            )}
          </div>
          <div style={{ display: "flex", gap: "50px", width: "400px", alignItems: "center", justifyContent: "center",marginTop:"40px" }}>
            {image && (<div style={{fontSize:"18px", fontWeight:"600",width:"200px",display:"flex",flexWrap:"wrap"}}>{text}</div>)}
            {image && (<div style={{fontSize:"18px", border:"2px solid white",backgroundColor:"white",color:"black", borderRadius:"5px"}}>{cta}</div>)}
          </div>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: "30px",marginTop:"30px" }}>
        <div style={{display:"flex",flexDirection:"column",textAlign:"center"}}>
        <div style={{fontSize:"19px",fontWeight:"600"}}>Ad Customization</div>
        <div>Customize your ad and get template according</div>
        </div>
        <div style={{ height: "50px", width: "500px", border: "1px solid lightgrey", borderRadius: "5px",display:"flex",alignItems:"center" }}>
          {/* <label htmlFor="file-input" >
            Choose a file
            <input id="file-input" type="file" onChange={handleImageChange} style={{cursor:"pointer"}} />
          </label> */}
          <div style={{marginLeft:"10px",display:"flex",alignItems:"center",justifyContent:"center"}}>
          <ImageIcon sx={{color:"lightblue"}}/>&nbsp; change and add creative image&nbsp;<label htmlFor="files" style={{color:"blue",textDecorationLine:"underline"}}>Select Image</label> <input id="files" type='file' style={{display:"none"}}  onChange={handleImageChange} />
          </div>
        </div>
        <div style={{textAlign:"center"}}>
        <div style={{opacity:"0.6"}}>-----------------------Edit content--------------------------</div>
        </div>
        <div>
          {/* <input type="text" placeholder='type' onChange={handletext}/> */}
          <TextField label="Ad Content" variant="outlined" onChange={handletext} sx={{ width: "500px" }} />
        </div>
        <div>
          {/* <input type="text" placeholder='type' onChange={handlecta}/> */}
          <TextField label="CTA" variant="outlined" onChange={handlecta} sx={{ width: "500px" }} />
        </div>
        <ColorPicker color={color} onChange={setColor} />;
      </div>
    </div>
  )
}

export default page;
