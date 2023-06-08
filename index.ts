import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import * as express from "express";

admin.initializeApp();

const app = express();

//////////////////ENTRANCE MODULE////////////////////////

app.get("/checkInStudent", async (req, res) => {
  try {
    const studentId = req.query.ID as string;

    const databaseRef = admin.database().ref(`Usuarios/${studentId}`);
    const studentSnapshot = await databaseRef.once("value");
    const studentData = studentSnapshot.val();

    if (!studentData) {
      return res.send("NO. control no registrado");
    }

    const checkedIn = studentData.CheckedIn;
    if (checkedIn == 1) {
      return res.send("Estudiante ya estacionado");
    }

    const lotSnapshot = await admin.database().ref("Lotes").once("value");
    const lotData = lotSnapshot.val();

    let lot: string | null = null;
    let espacio: string | null = null;

    // Iterate through the parking lots (A, B, C...)
    for (const lotKey in lotData) {
      const spacesData = lotData[lotKey];
      // Iterate through the parking spaces (1, 2, 3...)
      for (const spaceKey in spacesData) {
        const spaceValue = spacesData[spaceKey];
        if (spaceValue == 0) {
          lot = lotKey;
          espacio = spaceKey;
          await admin.database().ref(`Lotes/${lotKey}/${spaceKey}`).set(1);
          break;
        }
      }
      if (lot && espacio) {
        break;
      }
    }

    if (!lot || !espacio) {
      return res.send("No hay espacios disponibles");
    }

    await databaseRef.update({ CheckedIn: 1, Lote: lot, Espacio: espacio });

    const estacionamiento = `${lot}${espacio}`;
    const html = `<html><body style="background-color: #f1f1f1; font-family: Arial, sans-serif; text-align: center;"><h1 style="color: #333;">Estacionamiento asignado: <span style="color: #ff6600;">${estacionamiento}</span></h1></body></html>`;
    res.send(html);
  } catch (error) {
    console.error("Error processing request:", error);
    res.status(500).send("ERROR DESCONOCIDO");
  }
});

//////////////////GETTING OUT MODULE////////////////////////

app.get("/checkOutStudent", async (req, res) => {
  try {
    const studentId = req.query.ID as string;

    const databaseRef = admin.database().ref(`Usuarios/${studentId}`);
    const studentSnapshot = await databaseRef.once("value");
    const studentData = studentSnapshot.val();

    if (!studentData) {
      res.send("NO. control no registrado");
      return;
    }

    const checkedIn = studentData.CheckedIn;
    if (checkedIn != 1) {
      res.send("Estudiante no está estacionado");
      return;
    }

    const lot = studentData.Lote;
    const espacio = studentData.Espacio;

    await admin.database().ref(`Lotes/${lot}/${espacio}`).set(0);
    await databaseRef.update({ CheckedIn: 0, Lote: null, Espacio: null });

    res.send("Listo! Tenga un buen día!");
  } catch (error) {
    console.error("Error processing request:", error);
    res.status(500).send("ERROR DESCONOCIDO");
  }
});

// Serve the HTML page
app.use(express.static("public"));

// Expose the Express app as a Cloud Function
exports.app = functions.https.onRequest(app);
