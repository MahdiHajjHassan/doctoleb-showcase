export type Operation = {id:string;name:string;payload:any;role:string;created_at:string;error?:string;status?:string};
const DB_NAME='doctoleb-local-clinic-v1';
function database():Promise<IDBDatabase>{return new Promise((resolve,reject)=>{const request=indexedDB.open(DB_NAME,1);request.onupgradeneeded=()=>request.result.createObjectStore('workspace');request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);});}
export async function readWorkspace():Promise<{state:any;queue:Operation[]}>{const db=await database();try{return await new Promise((resolve,reject)=>{const tx=db.transaction('workspace','readonly');const request=tx.objectStore('workspace').get('current');request.onsuccess=()=>resolve(request.result || {state:null,queue:[]});request.onerror=()=>reject(request.error);});}finally{db.close();}}
export async function saveWorkspace(state:any,queue:Operation[]){const db=await database();try{await new Promise<void>((resolve,reject)=>{const tx=db.transaction('workspace','readwrite');tx.objectStore('workspace').put({state,queue},'current');tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);});}finally{db.close();}}
export function localChange(state:any,name:string,payload:any){
 const next=structuredClone(state);
 if(name==='create_patient')next.patients.push({...payload,archived:0,version:1,created_at:new Date().toISOString(),...(next.role!=='reception'?{encounters:[]}:{})});
 if(name==='update_patient'){next.patients=next.patients.map((p:any)=>p.id===payload.id?{...p,...payload,version:p.version+1}:p);next.appointments=next.appointments.map((a:any)=>a.patient_id===payload.id?{...a,patient_name:payload.name}:a);}
 if(name==='archive_patient')next.patients=next.patients.map((p:any)=>p.id===payload.id?{...p,archived:1,version:p.version+1}:p);
 if(name==='create_appointment')next.appointments.push({...payload,status:'scheduled',version:1,patient_name:next.patients.find((p:any)=>p.id===payload.patient_id)?.name});
 if(name==='set_status')next.appointments=next.appointments.map((a:any)=>a.id===payload.id?{...a,status:payload.status,version:a.version+1}:a);
 if(name==='save_encounter')next.patients=next.patients.map((p:any)=>p.id===payload.patient_id?{...p,version:p.version+1,encounters:[{...payload,created_at:new Date().toISOString(),author:next.doctors.find((d:any)=>d.id===next.appointments.find((a:any)=>a.id===payload.appointment_id)?.doctor_id)?.name},...(p.encounters || [])]}:p);
 return next;
}
