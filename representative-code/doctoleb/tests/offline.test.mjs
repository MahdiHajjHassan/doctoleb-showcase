import assert from 'node:assert/strict';
import test from 'node:test';
import {localChange} from '../src/offline.ts';

const workspace=()=>({role:'doctor',doctors:[{id:'doctor-1',name:'Dr. Noura Khalil'}],patients:[{id:'p-first',name:'First patient',version:1,encounters:[]}],appointments:[{id:'a-first',patient_id:'p-first',patient_name:'First patient',doctor_id:'doctor-1',status:'arrived',version:2}]});

test('offline registration and booking retain identifiers for ordered replay',()=>{
 const original=workspace();
 const withPatient=localChange(original,'create_patient',{id:'p-offline',name:'Rana Haddad'});
 const booked=localChange(withPatient,'create_appointment',{id:'a-offline',patient_id:'p-offline',doctor_id:'doctor-1',date:'2026-10-11',time:'16:00',duration:30,reason:'Follow-up'});
 const checked=localChange(booked,'set_status',{id:'a-offline',version:1,status:'arrived'});
 assert.equal(checked.patients.find(p=>p.id==='p-offline').version,1);
 assert.equal(checked.appointments.find(a=>a.id==='a-offline').patient_name,'Rana Haddad');
 assert.equal(checked.appointments.find(a=>a.id==='a-offline').version,2);
 assert.equal(original.patients.length,1);
});

test('offline encounter appears in history with the assigned doctor',()=>{
 const started=localChange(workspace(),'set_status',{id:'a-first',version:2,status:'in_progress'});
 const saved=localChange(started,'save_encounter',{id:'e-offline',patient_id:'p-first',appointment_id:'a-first',version:1,summary:'Follow-up',assessment:'Reviewed',plan:'Return in four weeks'});
 assert.equal(saved.patients[0].version,2);
 assert.equal(saved.patients[0].encounters[0].author,'Dr. Noura Khalil');
 assert.equal(saved.patients[0].encounters[0].plan,'Return in four weeks');
 assert.equal(saved.appointments[0].status,'in_progress');
});

test('offline patient rename immediately updates the schedule',()=>{
 const renamed=localChange(workspace(),'update_patient',{id:'p-first',name:'Updated name',version:1});
 assert.equal(renamed.patients[0].version,2);
 assert.equal(renamed.appointments[0].patient_name,'Updated name');
});
