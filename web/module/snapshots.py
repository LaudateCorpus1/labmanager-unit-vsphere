from sanic import Blueprint
import web.modeltr as data
import logging
import sanic.exceptions

from sanic import Blueprint

snapshots = Blueprint('snapshots')


# @snapshots.route('/machines/<machine_id>/snapshots', methods=['GET'])
# async def machines_deploy(request, machine_id):
#     return {'check': 'machines_get_snapshots {}, rq: {}'.format(machine_id, request.headers)}

@snapshots.route('/machines/<machine_id>/snapshots', methods=['POST'])
async def take_snapshot(request, machine_id):
    with data.Connection.use() as conn:

        snapshot_name = request.headers['json_params']['name']

        machine = data.Machine.get_one_for_update({'_id': machine_id}, conn=conn)
        new_snapshot = data.Snapshot(machine=machine_id, name=snapshot_name)
        new_snapshot.save(conn=conn)

        machine.snapshots.append(new_snapshot.id)
        machine.save(conn=conn)

        new_request = data.Request(state='created', type='take_snapshot')
        new_request.machine = machine.id
        new_request.subject_id = new_snapshot.id
        new_request.save(conn=conn)

        # begin snapshot preparation
        data.Action(type='other', request=new_request.id).save(conn=conn)
    return {
        'result': {
            'snapshot_id': new_snapshot.id,
        },
        'is_last': True,
    }

@snapshots.route('/machines/<machine_id>/snapshots/<snapshot_id>', methods=['PUT'])
async def restore_snapshot(request, machine_id, snapshot_id):
    with data.Connection.use() as conn:
        action = request.headers['json_params'].get('action')
        if action is None:
            raise sanic.exceptions.InvalidUsage('\'action\' is missing in passed data!')
        elif action == 'restore':
            machine_ro = data.Machine.get_one({'_id': machine_id}, conn=conn)
            new_request = data.Request(state='created', type='restore_snapshot')
            new_request.machine = machine_ro.id
            new_request.subject_id = snapshot_id
            new_request.save(conn=conn)

            # begin snapshot restoration
            data.Action(type='other', request=new_request.id).save(conn=conn)

            # TODO what to return?
            return {
                'result': {'snapshot_id': snapshot_id},
                'is_last': True,
            }

        else:
            raise sanic.exceptions.InvalidUsage(f'Invalid \'action\' value: {action}')

